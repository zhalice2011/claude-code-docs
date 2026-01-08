#!/usr/bin/env python3
"""
Unit tests for the multi-source Claude documentation fetcher.

Run with: python -m pytest test_fetch_claude_docs.py -v
Or simply: python test_fetch_claude_docs.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import json
import hashlib
import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_claude_docs import (
    url_to_safe_filename,
    validate_markdown_content,
    content_has_changed,
    load_manifest,
    save_manifest,
    discover_pages_from_sitemap,
    DOC_SOURCES,
    MANIFEST_FILE,
)


class TestUrlToSafeFilename(unittest.TestCase):
    """Test cases for url_to_safe_filename function."""

    def test_simple_path_claude_code(self):
        """Test simple path without subdirectories for claude-code docs."""
        prefixes = ['/docs/en/', '/en/docs/claude-code/']
        result = url_to_safe_filename('/docs/en/hooks', prefixes)
        self.assertEqual(result, 'hooks.md')

    def test_simple_path_platform(self):
        """Test simple path for platform docs."""
        prefixes = ['/docs/en/']
        result = url_to_safe_filename('/docs/en/intro', prefixes)
        self.assertEqual(result, 'intro.md')

    def test_nested_path_platform(self):
        """Test nested path for platform docs (e.g., agents-and-tools/tool-use/bash-tool)."""
        prefixes = ['/docs/en/']
        result = url_to_safe_filename('/docs/en/agents-and-tools/tool-use/bash-tool', prefixes)
        self.assertEqual(result, 'agents-and-tools__tool-use__bash-tool.md')

    def test_deeply_nested_path(self):
        """Test deeply nested path."""
        prefixes = ['/docs/en/']
        result = url_to_safe_filename('/docs/en/a/b/c/d', prefixes)
        self.assertEqual(result, 'a__b__c__d.md')

    def test_path_already_has_md_extension(self):
        """Test path that already has .md extension."""
        prefixes = ['/docs/en/']
        result = url_to_safe_filename('/docs/en/hooks.md', prefixes)
        # Should not add double .md
        self.assertTrue(result.endswith('.md'))
        self.assertFalse(result.endswith('.md.md'))

    def test_legacy_claude_code_prefix(self):
        """Test legacy claude-code path prefix."""
        prefixes = ['/docs/en/', '/en/docs/claude-code/']
        result = url_to_safe_filename('/en/docs/claude-code/memory', prefixes)
        self.assertEqual(result, 'memory.md')

    def test_path_with_trailing_slash(self):
        """Test path with trailing slash."""
        prefixes = ['/docs/en/']
        result = url_to_safe_filename('/docs/en/hooks/', prefixes)
        self.assertEqual(result, 'hooks.md')

    def test_no_matching_prefix_fallback(self):
        """Test fallback behavior when no prefix matches."""
        prefixes = ['/some/other/prefix/']
        result = url_to_safe_filename('/docs/en/hooks', prefixes)
        # Should still produce a valid filename
        self.assertTrue(result.endswith('.md'))


class TestValidateMarkdownContent(unittest.TestCase):
    """Test cases for validate_markdown_content function."""

    def test_valid_markdown(self):
        """Test valid markdown content passes validation."""
        content = """# Test Document

This is a test document with some content.

## Section 1

- Item 1
- Item 2
- Item 3

```python
def hello():
    print("Hello, world!")
```

For more information, see [the documentation](https://example.com).
"""
        # Should not raise
        validate_markdown_content(content, 'test.md')

    def test_html_content_rejected(self):
        """Test HTML content is rejected."""
        content = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>Hello</body>
</html>"""
        with self.assertRaises(ValueError) as context:
            validate_markdown_content(content, 'test.md')
        self.assertIn('HTML', str(context.exception))

    def test_short_content_rejected(self):
        """Test very short content is rejected."""
        content = "Short"
        with self.assertRaises(ValueError) as context:
            validate_markdown_content(content, 'test.md')
        self.assertIn('too short', str(context.exception))

    def test_empty_content_rejected(self):
        """Test empty content is rejected."""
        with self.assertRaises(ValueError):
            validate_markdown_content('', 'test.md')

    def test_non_markdown_content_rejected(self):
        """Test content without markdown indicators is rejected."""
        content = """This is just plain text without any markdown formatting.
It has multiple lines but no headers, lists, code blocks, or links.
Just plain text content that goes on and on.
More plain text here to make it long enough.
Even more text to pass the length check.
"""
        with self.assertRaises(ValueError) as context:
            validate_markdown_content(content, 'test.md')
        self.assertIn('markdown', str(context.exception).lower())


class TestContentHasChanged(unittest.TestCase):
    """Test cases for content_has_changed function."""

    def test_same_content(self):
        """Test same content returns False."""
        content = "# Test\n\nSome content here."
        hash_val = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self.assertFalse(content_has_changed(content, hash_val))

    def test_different_content(self):
        """Test different content returns True."""
        content1 = "# Test\n\nSome content here."
        content2 = "# Test\n\nDifferent content here."
        hash_val = hashlib.sha256(content1.encode('utf-8')).hexdigest()
        self.assertTrue(content_has_changed(content2, hash_val))

    def test_empty_old_hash(self):
        """Test empty old hash always returns True (new content)."""
        content = "# Test\n\nSome content here."
        self.assertTrue(content_has_changed(content, ''))


class TestManifestOperations(unittest.TestCase):
    """Test cases for manifest load/save operations."""

    def setUp(self):
        """Set up temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.docs_dir = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_manifest_not_exists(self):
        """Test loading manifest when file doesn't exist."""
        manifest = load_manifest(self.docs_dir)
        self.assertEqual(manifest, {"files": {}, "last_updated": None})

    def test_load_manifest_exists(self):
        """Test loading existing manifest."""
        test_manifest = {
            "files": {
                "test.md": {
                    "hash": "abc123",
                    "last_updated": "2024-01-01T00:00:00"
                }
            },
            "last_updated": "2024-01-01T00:00:00"
        }
        manifest_path = self.docs_dir / MANIFEST_FILE
        manifest_path.write_text(json.dumps(test_manifest))

        loaded = load_manifest(self.docs_dir)
        self.assertEqual(loaded["files"]["test.md"]["hash"], "abc123")

    def test_load_manifest_invalid_json(self):
        """Test loading manifest with invalid JSON."""
        manifest_path = self.docs_dir / MANIFEST_FILE
        manifest_path.write_text("not valid json {{{")

        manifest = load_manifest(self.docs_dir)
        self.assertEqual(manifest, {"files": {}, "last_updated": None})

    def test_save_manifest(self):
        """Test saving manifest."""
        test_manifest = {
            "files": {
                "test.md": {
                    "hash": "abc123",
                    "last_updated": "2024-01-01T00:00:00"
                }
            }
        }
        source_config = {
            "name": "test-source",
            "output_dir": "docs/test",
            "official_docs_base": "https://example.com/docs"
        }

        save_manifest(self.docs_dir, test_manifest, source_config)

        manifest_path = self.docs_dir / MANIFEST_FILE
        self.assertTrue(manifest_path.exists())

        loaded = json.loads(manifest_path.read_text())
        self.assertIn("last_updated", loaded)
        self.assertEqual(loaded["source_name"], "test-source")


class TestDocSourcesConfiguration(unittest.TestCase):
    """Test cases for DOC_SOURCES configuration."""

    def test_doc_sources_not_empty(self):
        """Test DOC_SOURCES is not empty."""
        self.assertGreater(len(DOC_SOURCES), 0)

    def test_claude_code_source_exists(self):
        """Test claude-code source exists."""
        names = [s["name"] for s in DOC_SOURCES]
        self.assertIn("claude-code", names)

    def test_platform_source_exists(self):
        """Test platform source exists."""
        names = [s["name"] for s in DOC_SOURCES]
        self.assertIn("platform", names)

    def test_required_fields_present(self):
        """Test all required fields are present in each source."""
        required_fields = [
            "name",
            "description",
            "sitemap_urls",
            "output_dir",
            "english_patterns",
            "path_prefixes",
            "manifest_file",
        ]
        for source in DOC_SOURCES:
            for field in required_fields:
                self.assertIn(field, source, f"Missing field '{field}' in source '{source.get('name', 'unknown')}'")

    def test_output_dirs_are_different(self):
        """Test each source has a unique output directory."""
        output_dirs = [s["output_dir"] for s in DOC_SOURCES]
        self.assertEqual(len(output_dirs), len(set(output_dirs)), "Duplicate output directories found")

    def test_claude_code_has_changelog(self):
        """Test claude-code source has fetch_changelog enabled."""
        claude_code = next(s for s in DOC_SOURCES if s["name"] == "claude-code")
        self.assertTrue(claude_code.get("fetch_changelog", False))

    def test_platform_no_changelog(self):
        """Test platform source does not have fetch_changelog enabled."""
        platform = next(s for s in DOC_SOURCES if s["name"] == "platform")
        self.assertFalse(platform.get("fetch_changelog", False))


class TestDiscoverPagesFromSitemap(unittest.TestCase):
    """Test cases for discover_pages_from_sitemap function."""

    def test_parse_valid_sitemap(self):
        """Test parsing a valid sitemap XML."""
        sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/docs/en/intro</loc>
    </url>
    <url>
        <loc>https://example.com/docs/en/setup</loc>
    </url>
    <url>
        <loc>https://example.com/docs/de/intro</loc>
    </url>
</urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml.encode('utf-8')
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        pages = discover_pages_from_sitemap(
            mock_session,
            "https://example.com/sitemap.xml",
            english_patterns=["/docs/en/"],
            skip_patterns=[]
        )

        # Should only include English pages
        self.assertEqual(len(pages), 2)
        self.assertIn("/docs/en/intro", pages)
        self.assertIn("/docs/en/setup", pages)
        # German page should be excluded
        self.assertNotIn("/docs/de/intro", pages)

    def test_skip_patterns(self):
        """Test skip patterns filter out unwanted pages."""
        sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/docs/en/intro</loc>
    </url>
    <url>
        <loc>https://example.com/docs/en/api/reference</loc>
    </url>
    <url>
        <loc>https://example.com/docs/en/examples/demo</loc>
    </url>
</urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml.encode('utf-8')
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        pages = discover_pages_from_sitemap(
            mock_session,
            "https://example.com/sitemap.xml",
            english_patterns=["/docs/en/"],
            skip_patterns=["/api/", "/examples/"]
        )

        self.assertEqual(len(pages), 1)
        self.assertIn("/docs/en/intro", pages)

    def test_empty_sitemap(self):
        """Test handling of empty sitemap."""
        sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml.encode('utf-8')
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        pages = discover_pages_from_sitemap(
            mock_session,
            "https://example.com/sitemap.xml",
            english_patterns=["/docs/en/"],
            skip_patterns=[]
        )

        self.assertEqual(len(pages), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the fetcher."""

    def test_url_conversion_matches_expected_filenames(self):
        """Test URL to filename conversion produces expected results."""
        # Claude Code docs
        claude_prefixes = DOC_SOURCES[0]["path_prefixes"]

        test_cases = [
            ("/docs/en/hooks", "hooks.md"),
            ("/docs/en/memory", "memory.md"),
            ("/docs/en/mcp", "mcp.md"),
        ]

        for url_path, expected in test_cases:
            result = url_to_safe_filename(url_path, claude_prefixes)
            self.assertEqual(result, expected, f"Failed for {url_path}")

    def test_platform_url_conversion(self):
        """Test platform URL to filename conversion."""
        platform_prefixes = DOC_SOURCES[1]["path_prefixes"]

        test_cases = [
            ("/docs/en/intro", "intro.md"),
            ("/docs/en/about-claude/models/overview", "about-claude__models__overview.md"),
            ("/docs/en/agents-and-tools/tool-use/bash-tool", "agents-and-tools__tool-use__bash-tool.md"),
        ]

        for url_path, expected in test_cases:
            result = url_to_safe_filename(url_path, platform_prefixes)
            self.assertEqual(result, expected, f"Failed for {url_path}")


class TestHelperScriptIntegration(unittest.TestCase):
    """Tests for helper script compatibility."""

    def test_double_underscore_to_slash_conversion(self):
        """Test that filenames with __ can be converted back to URL paths."""
        # This is important for the helper script's URL generation
        filename = "agents-and-tools__tool-use__bash-tool.md"

        # Remove .md extension
        topic = filename[:-3]

        # Convert __ back to /
        url_path = topic.replace("__", "/")

        self.assertEqual(url_path, "agents-and-tools/tool-use/bash-tool")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
