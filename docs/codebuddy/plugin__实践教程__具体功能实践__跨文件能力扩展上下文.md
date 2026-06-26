本文会基于一个实战的评测剖析，来介绍如何通过跨文件让补全内容来扩展更多的上下文，从而让生成代码质量更高更准。

为了提高生成质量，引入更多的上下文信息是很有必要的。在代码补全的场景中，除了当前文件的内容，还需要收集与之相关的更多代码作为上下文，并对提示词进行优化。本文将通过腾讯云代码助手的实例，详细介绍如何实时扩展上下文，获取更多跨文件的内容，以实现准确的代码补全。

## 如何让补全感知更多

整体思路是，考虑到开发人员在编码时会下意识地思考相关内容，所以设计也会比较简单。即优先选择打开的文件，通过算法判定这些文件和当前光标上下文的关联，从而给到模型进行排名和相似度计算。

所以，第一步是个工程问题。提取所有可能相关的上下文，可能是当前文件、导入的文件、同一目录中的文件等中的代码等。

接下来，第二步是重新排名和相似度计算。具体的选择思路如下：离线场景选取文件的时候，会根据文件结构进行选择，在目录结构中越紧邻的文件越容易被选到；上线场景选择文件的时候，可以根据用户在编辑器中打开的文件进行选择，选择用户最近打开的n个文件；代码片段的选择思路，是根据 TF\-IDF（一种信息检索领域的常用算法）进行代码片段的相关性匹配，选取比较相关的一段代码。

最后，通过按排名顺序添加上下文片段来构建提示，直到填充代码补全模型的最大上下文长度。还有一些其他细节可确保模型将这些理解为不同的信息片段，但一旦构建完成，这些细节就会被发送到模型进行推理。

举例：

java
```
<reponame>reponame + <neighbor><filename>file_name<codeblock>code_block * (n) + <filename>filename<fim_prefix>code_prefix<fim_suffix>code_suffix<fim_middle>code_middle<endoftext>
```
## 实战代码助手 \- 跨文件能力

按以下步骤实践跨文件能力。下图是项目局部图，entity 定义了三个对象，他们彼此有对象关联。同时 User 类里的 ZipCode 需要从一个单例工厂中创建获得。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/b929a2c2e21611eeb1eb525400b5f95f.png)

实体类大概是这样的：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/ca0d7494e21611ee9ca3525400bb593a.png)

### 任务一：申明几个对象关联关系，看补全里是否自动插入了另一个文件的函数

打开 User.java、PhotoArts.java、Image.java，在 UserServiceImpl.java 里创建一个函数，通过跨文件的延展，可以正确生成多个文件的函数调用链。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6ada6fa115db11f0854e525400454e06.png)

视频如下：

### 任务二： 申明的单例模式的工厂类，看补全里是否正确获取调用单例工厂的函数

定义了一个 CityFactory，它是一个单例工厂，用于转 ZipCode 方法。代码如下：

java
```

public class CityFactory {
    private CityFactory() {
    }

    private static class CityFactoryHolder {
        private static CityFactory INSTANCE = new CityFactory();
    }

    public static CityFactory getInstance() {
        if (CityFactoryHolder.INSTANCE == null) {
            synchronized (CityFactory.class) {
                if (CityFactoryHolder.INSTANCE == null) {
                    CityFactoryHolder.INSTANCE = new CityFactory();
                }
            }
        }
        return CityFactoryHolder.INSTANCE;
    }

    public String getZipCodeByCity(String cityId) {
        // load from database
        // connect from database
        return "12345";
    }

}
```
通过查看补全内容，可以确定代码助手正确的理解了工厂类的调用，而不是简单的实例化。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/5d5b5c72e21711eeb1eb525400b5f95f.png)

## 实战演示效果

## 总结

本文用简单的示例，来看出跨文件补全的产品价值。结合中间补全（Fill\-in\-Middle）机制，并扩展上下文的窗口， 引入更多的想关联的文件，从而让补全生成更精准，也更接近对项目工程当下的情境理解。