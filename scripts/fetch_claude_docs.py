#!/usr/bin/env python3
"""
Multi-source Claude documentation fetcher with support for:
- Claude Code docs (code.claude.com)
- Claude Platform docs (platform.claude.com)

Version 4.0 - Added multi-source support
"""

import requests
import time
from pathlib import Path
from typing import List, Tuple, Set, Optional, Dict, Any
import logging
from datetime import datetime
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import json
import hashlib
import os
import re
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION: Documentation Sources
# =============================================================================
# Each source is processed independently with its own output directory and manifest

DOC_SOURCES = [
    {
        "name": "claude-code",
        "description": "Claude Code CLI documentation",
        "sitemap_urls": [
            "https://code.claude.com/docs/sitemap.xml",
            "https://docs.anthropic.com/sitemap.xml",  # Legacy fallback
        ],
        "output_dir": "docs",
        "english_patterns": ["/docs/en/", "/en/docs/claude-code/"],
        "path_prefixes": ["/docs/en/", "/en/docs/claude-code/", "/docs/claude-code/", "/claude-code/"],
        "skip_patterns": ["/tool-use/", "/examples/", "/legacy/", "/api/", "/reference/"],
        "manifest_file": "docs_manifest.json",
        "fetch_changelog": True,
        "official_docs_base": "https://docs.anthropic.com/en/docs/claude-code",
    },
    {
        "name": "platform",
        "description": "Claude Platform API documentation",
        "sitemap_urls": [
            "https://platform.claude.com/sitemap.xml",
        ],
        "output_dir": "docs/platform",
        "english_patterns": ["/docs/en/"],
        "path_prefixes": ["/docs/en/"],
        "skip_patterns": [],  # Platform docs - include everything
        "manifest_file": "docs_manifest.json",
        "fetch_changelog": False,
        "official_docs_base": "https://platform.claude.com/docs/en",
    },
]

# =============================================================================
# CONSTANTS
# =============================================================================

MANIFEST_FILE = "docs_manifest.json"

# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/4.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay in seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# =============================================================================
# MANIFEST FUNCTIONS
# =============================================================================

def load_manifest(docs_dir: Path) -> dict:
    """Load the manifest of previously fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            if "files" not in manifest:
                manifest["files"] = {}
            return manifest
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
    return {"files": {}, "last_updated": None}


def save_manifest(docs_dir: Path, manifest: dict, source_config: dict) -> None:
    """Save the manifest of fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    manifest["last_updated"] = datetime.now().isoformat()

    # Get GitHub repository from environment or use default
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'ericbuess/claude-code-docs')
    github_ref = os.environ.get('GITHUB_REF_NAME', 'main')

    # Validate repository name format
    if not re.match(r'^[\w.-]+/[\w.-]+$', github_repo):
        logger.warning(f"Invalid repository format: {github_repo}, using default")
        github_repo = 'ericbuess/claude-code-docs'

    if not re.match(r'^[\w.-]+$', github_ref):
        logger.warning(f"Invalid ref format: {github_ref}, using default")
        github_ref = 'main'

    # Calculate relative path from repo root
    relative_output = source_config["output_dir"]
    manifest["base_url"] = f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/{relative_output}/"
    manifest["github_repository"] = github_repo
    manifest["github_ref"] = github_ref
    manifest["source_name"] = source_config["name"]
    manifest["official_docs_base"] = source_config.get("official_docs_base", "")
    manifest["description"] = f"Claude {source_config['name']} documentation manifest."
    manifest_path.write_text(json.dumps(manifest, indent=2))


# =============================================================================
# FILENAME CONVERSION
# =============================================================================

def url_to_safe_filename(url_path: str, path_prefixes: List[str] = None) -> str:
    """
    Convert a URL path to a safe filename.

    Args:
        url_path: The URL path to convert
        path_prefixes: List of prefixes to strip from the path

    Returns:
        A safe filename with .md extension
    """
    if path_prefixes is None:
        path_prefixes = ['/docs/en/', '/en/docs/claude-code/', '/docs/claude-code/', '/claude-code/']

    # Remove any known prefix patterns
    path = url_path
    for prefix in path_prefixes:
        if prefix in url_path:
            path = url_path.split(prefix)[-1]
            break
    else:
        # If no known prefix, try common patterns
        for pattern in ['claude-code/', 'docs/']:
            if pattern in url_path:
                path = url_path.split(pattern)[-1]
                break

    # Clean up trailing slashes
    path = path.strip('/')

    # If no subdirectories, just use the filename
    if '/' not in path:
        return path + '.md' if not path.endswith('.md') else path

    # For subdirectories, replace slashes with double underscores
    # e.g., "advanced/setup" becomes "advanced__setup.md"
    safe_name = path.replace('/', '__')
    if not safe_name.endswith('.md'):
        safe_name += '.md'
    return safe_name


# =============================================================================
# SITEMAP DISCOVERY
# =============================================================================

def discover_sitemap_and_base_url(session: requests.Session, sitemap_urls: List[str]) -> Tuple[str, str]:
    """
    Discover the sitemap URL and extract the base URL from it.

    Args:
        session: requests Session object
        sitemap_urls: List of sitemap URLs to try

    Returns:
        Tuple of (sitemap_url, base_url)
    """
    for sitemap_url in sitemap_urls:
        try:
            logger.info(f"Trying sitemap: {sitemap_url}")
            response = session.get(sitemap_url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                # Extract base URL from sitemap URL
                parsed = urlparse(sitemap_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
                logger.info(f"Found sitemap at {sitemap_url}, base URL: {base_url}")
                return sitemap_url, base_url
        except Exception as e:
            logger.warning(f"Failed to fetch {sitemap_url}: {e}")
            continue

    raise Exception("Could not find a valid sitemap")


def discover_pages_from_sitemap(
    session: requests.Session,
    sitemap_url: str,
    english_patterns: List[str],
    skip_patterns: List[str]
) -> List[str]:
    """
    Dynamically discover documentation pages from the sitemap.

    Args:
        session: requests Session object
        sitemap_url: URL of the sitemap
        english_patterns: Patterns to match English documentation
        skip_patterns: Patterns to skip

    Returns:
        List of documentation page paths
    """
    logger.info(f"Discovering documentation pages from {sitemap_url}...")

    try:
        response = session.get(sitemap_url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # Parse XML sitemap safely
        try:
            parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)
            root = ET.fromstring(response.content, parser=parser)
        except TypeError:
            logger.warning("XMLParser security parameters not available, using default parser")
            root = ET.fromstring(response.content)

        # Extract all URLs from sitemap
        urls = []
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for url_elem in root.findall('.//ns:url', namespace):
            loc_elem = url_elem.find('ns:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text)

        # If no URLs found with namespace, try without
        if not urls:
            for loc_elem in root.findall('.//loc'):
                if loc_elem.text:
                    urls.append(loc_elem.text)

        logger.info(f"Found {len(urls)} total URLs in sitemap")

        # Filter for ENGLISH documentation pages only
        doc_pages = []
        for url in urls:
            # Check if URL matches English pattern
            if any(pattern in url for pattern in english_patterns):
                parsed = urlparse(url)
                path = parsed.path

                # Remove any file extension
                if path.endswith('.html'):
                    path = path[:-5]
                elif path.endswith('/'):
                    path = path[:-1]

                # Skip certain types of pages
                if skip_patterns and any(skip in path for skip in skip_patterns):
                    continue

                doc_pages.append(path)

        # Remove duplicates and sort
        doc_pages = sorted(list(set(doc_pages)))

        logger.info(f"Discovered {len(doc_pages)} documentation pages")
        return doc_pages

    except Exception as e:
        logger.error(f"Failed to discover pages from sitemap: {e}")
        return []


# =============================================================================
# CONTENT VALIDATION
# =============================================================================

def validate_markdown_content(content: str, filename: str) -> None:
    """
    Validate that content is proper markdown.
    Raises ValueError if validation fails.
    """
    # Check for HTML content
    if not content or content.startswith('<!DOCTYPE') or '<html' in content[:100]:
        raise ValueError("Received HTML instead of markdown")

    # Check minimum length
    if len(content.strip()) < 50:
        raise ValueError(f"Content too short ({len(content)} bytes)")

    # Check for common markdown elements
    lines = content.split('\n')
    markdown_indicators = [
        '# ', '## ', '### ',  # Headers
        '```',                 # Code blocks
        '- ', '* ', '1. ',    # Lists
        '[', '**', '_', '> ', # Links, bold, italic, quotes
    ]

    # Count markdown indicators
    indicator_count = 0
    for line in lines[:50]:
        for indicator in markdown_indicators:
            if line.strip().startswith(indicator) or indicator in line:
                indicator_count += 1
                break

    # Require at least some markdown formatting
    if indicator_count < 3:
        raise ValueError(f"Content doesn't appear to be markdown (only {indicator_count} indicators found)")


# =============================================================================
# CONTENT FETCHING
# =============================================================================

def fetch_markdown_content(path: str, session: requests.Session, base_url: str) -> Tuple[str, str]:
    """
    Fetch markdown content with error handling and validation.

    Args:
        path: URL path to fetch
        session: requests Session object
        base_url: Base URL for the documentation

    Returns:
        Tuple of (filename, content)
    """
    markdown_url = f"{base_url}{path}.md"

    logger.info(f"Fetching: {markdown_url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(markdown_url, headers=HEADERS, timeout=30, allow_redirects=True)

            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            content = response.text
            validate_markdown_content(content, path)

            logger.info(f"Successfully fetched {path} ({len(content)} bytes)")
            return path, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {path}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.info(f"Retrying in {jittered_delay:.1f} seconds...")
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch {path} after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Content validation failed for {path}: {e}")
            raise


def fetch_changelog(session: requests.Session) -> Tuple[str, str]:
    """
    Fetch Claude Code changelog from GitHub repository.
    Returns tuple of (filename, content).
    """
    changelog_url = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
    filename = "changelog.md"

    logger.info(f"Fetching Claude Code changelog: {changelog_url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(changelog_url, headers=HEADERS, timeout=30, allow_redirects=True)

            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            content = response.text

            # Add header
            header = """# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
>
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository.

---

"""
            content = header + content

            if len(content.strip()) < 100:
                raise ValueError(f"Changelog content too short ({len(content)} bytes)")

            logger.info(f"Successfully fetched changelog ({len(content)} bytes)")
            return filename, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for changelog: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch changelog after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Changelog validation failed: {e}")
            raise


def content_has_changed(content: str, old_hash: str) -> bool:
    """Check if content has changed based on hash."""
    new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return new_hash != old_hash


# =============================================================================
# FILE OPERATIONS
# =============================================================================

def save_markdown_file(docs_dir: Path, filename: str, content: str) -> str:
    """Save markdown content and return its hash."""
    file_path = docs_dir / filename

    try:
        file_path.write_text(content, encoding='utf-8')
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        logger.info(f"Saved: {filename}")
        return content_hash
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def cleanup_old_files(docs_dir: Path, current_files: Set[str], manifest: dict) -> None:
    """
    Remove only files that were previously fetched but no longer exist.
    Preserves manually added files.
    """
    previous_files = set(manifest.get("files", {}).keys())
    files_to_remove = previous_files - current_files

    for filename in files_to_remove:
        if filename == MANIFEST_FILE:
            continue

        file_path = docs_dir / filename
        if file_path.exists():
            logger.info(f"Removing obsolete file: {filename}")
            file_path.unlink()


# =============================================================================
# SOURCE PROCESSING
# =============================================================================

def process_doc_source(source_config: dict, session: requests.Session, repo_root: Path) -> dict:
    """
    Process a single documentation source.

    Args:
        source_config: Configuration for the documentation source
        session: requests Session object
        repo_root: Path to the repository root

    Returns:
        Dictionary with processing statistics
    """
    source_name = source_config["name"]
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing source: {source_name} - {source_config['description']}")
    logger.info(f"{'='*60}")

    # Create output directory
    docs_dir = repo_root / source_config["output_dir"]
    docs_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")

    # Load manifest for this source
    manifest = load_manifest(docs_dir)

    # Stats
    stats = {
        "source_name": source_name,
        "successful": 0,
        "failed": 0,
        "failed_pages": [],
        "fetched_files": set(),
        "pages_discovered": 0,
    }
    new_manifest = {"files": {}}

    # Discover sitemap and base URL
    try:
        sitemap_url, base_url = discover_sitemap_and_base_url(session, source_config["sitemap_urls"])
    except Exception as e:
        logger.error(f"Failed to discover sitemap for {source_name}: {e}")
        return stats

    # Discover pages
    doc_pages = discover_pages_from_sitemap(
        session,
        sitemap_url,
        source_config["english_patterns"],
        source_config.get("skip_patterns", [])
    )

    stats["pages_discovered"] = len(doc_pages)

    if not doc_pages:
        logger.error(f"No documentation pages discovered for {source_name}")
        return stats

    # Fetch each page
    for i, page_path in enumerate(doc_pages, 1):
        logger.info(f"[{source_name}] Processing {i}/{len(doc_pages)}: {page_path}")

        try:
            _, content = fetch_markdown_content(page_path, session, base_url)

            # Convert to safe filename using source-specific prefixes
            filename = url_to_safe_filename(page_path, source_config["path_prefixes"])

            # Check if content has changed
            old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
            old_entry = manifest.get("files", {}).get(filename, {})

            if content_has_changed(content, old_hash):
                content_hash = save_markdown_file(docs_dir, filename, content)
                logger.info(f"Updated: {filename}")
                last_updated = datetime.now().isoformat()
            else:
                content_hash = old_hash
                logger.info(f"Unchanged: {filename}")
                last_updated = old_entry.get("last_updated", datetime.now().isoformat())

            new_manifest["files"][filename] = {
                "original_url": f"{base_url}{page_path}",
                "original_md_url": f"{base_url}{page_path}.md",
                "hash": content_hash,
                "last_updated": last_updated,
                "source": source_name
            }

            stats["fetched_files"].add(filename)
            stats["successful"] += 1

            # Rate limiting
            if i < len(doc_pages):
                time.sleep(RATE_LIMIT_DELAY)

        except Exception as e:
            logger.error(f"Failed to process {page_path}: {e}")
            stats["failed"] += 1
            stats["failed_pages"].append(page_path)

    # Fetch changelog if configured
    if source_config.get("fetch_changelog", False):
        logger.info("Fetching Claude Code changelog...")
        try:
            filename, content = fetch_changelog(session)

            old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
            old_entry = manifest.get("files", {}).get(filename, {})

            if content_has_changed(content, old_hash):
                content_hash = save_markdown_file(docs_dir, filename, content)
                logger.info(f"Updated: {filename}")
                last_updated = datetime.now().isoformat()
            else:
                content_hash = old_hash
                logger.info(f"Unchanged: {filename}")
                last_updated = old_entry.get("last_updated", datetime.now().isoformat())

            new_manifest["files"][filename] = {
                "original_url": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
                "original_raw_url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
                "hash": content_hash,
                "last_updated": last_updated,
                "source": "claude-code-repository"
            }

            stats["fetched_files"].add(filename)
            stats["successful"] += 1

        except Exception as e:
            logger.error(f"Failed to fetch changelog: {e}")
            stats["failed"] += 1
            stats["failed_pages"].append("changelog")

    # Clean up old files
    cleanup_old_files(docs_dir, stats["fetched_files"], manifest)

    # Add metadata and save manifest
    new_manifest["fetch_metadata"] = {
        "source_name": source_name,
        "last_fetch_completed": datetime.now().isoformat(),
        "sitemap_url": sitemap_url,
        "base_url": base_url,
        "pages_discovered": stats["pages_discovered"],
        "pages_fetched_successfully": stats["successful"],
        "pages_failed": stats["failed"],
        "failed_pages": stats["failed_pages"],
        "total_files": len(stats["fetched_files"]),
        "fetch_tool_version": "4.0"
    }
    save_manifest(docs_dir, new_manifest, source_config)

    # Log source summary
    logger.info(f"\n[{source_name}] Summary:")
    logger.info(f"  Discovered: {stats['pages_discovered']} pages")
    logger.info(f"  Successful: {stats['successful']}")
    logger.info(f"  Failed: {stats['failed']}")

    return stats


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main function - processes all configured doc sources."""
    start_time = datetime.now()
    logger.info("Starting Claude documentation fetch (multi-source version 4.0)")

    # Log configuration
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'ericbuess/claude-code-docs')
    logger.info(f"GitHub repository: {github_repo}")

    # Get repository root (parent of scripts directory)
    repo_root = Path(__file__).parent.parent
    logger.info(f"Repository root: {repo_root}")

    # Check for source filter from command line
    source_filter = None
    if len(sys.argv) > 1:
        source_filter = sys.argv[1]
        logger.info(f"Filtering to source: {source_filter}")

    # Aggregate statistics
    total_stats = {
        "successful": 0,
        "failed": 0,
        "failed_pages": [],
        "sources_processed": 0,
    }

    with requests.Session() as session:
        for source_config in DOC_SOURCES:
            # Skip if source filter is specified and doesn't match
            if source_filter and source_config["name"] != source_filter:
                logger.info(f"Skipping source: {source_config['name']} (filtered)")
                continue

            stats = process_doc_source(source_config, session, repo_root)

            total_stats["successful"] += stats["successful"]
            total_stats["failed"] += stats["failed"]
            total_stats["failed_pages"].extend(stats["failed_pages"])
            total_stats["sources_processed"] += 1

    # Final summary
    duration = datetime.now() - start_time
    logger.info("\n" + "="*60)
    logger.info("FINAL SUMMARY")
    logger.info("="*60)
    logger.info(f"Duration: {duration}")
    logger.info(f"Sources processed: {total_stats['sources_processed']}")
    logger.info(f"Total successful: {total_stats['successful']}")
    logger.info(f"Total failed: {total_stats['failed']}")

    if total_stats["failed_pages"]:
        logger.warning("\nFailed pages (will retry next run):")
        for page in total_stats["failed_pages"]:
            logger.warning(f"  - {page}")

        if total_stats["successful"] == 0:
            logger.error("No pages were fetched successfully!")
            sys.exit(1)
    else:
        logger.info("\nAll pages fetched successfully!")


if __name__ == "__main__":
    main()
