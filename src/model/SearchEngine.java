package model;

import org.apache.commons.io.FileUtils;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystems;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class SearchEngine {
    private static final String CN_FILE_PATH = "C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\New_CN";
    private static final String EN_FILE_PATH = "C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\New_EN";

    private static final String INDEX_CN = "C:\\Users\\McFly\\Documents\\Java IDEA\\controller.SearchEngine\\index\\index_chinese";
    private static final String INDEX_EN = "C:\\Users\\McFly\\Documents\\Java IDEA\\controller.SearchEngine\\index\\index_english";

    private List<String> searchResult = null;

    /**
     * @Title:SearchEngine
     * @Description:构造函数
     */
    public SearchEngine() {
        searchResult = new ArrayList<>();
    }

    public void createCNIndex() {
        Directory directory = null;
        IndexWriter indexWriter = null;
        Document document = null;
        try {
            directory = FSDirectory.open(FileSystems.getDefault().getPath(INDEX_CN));
            Analyzer analyzer = new SmartChineseAnalyzer();
            IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(directory, indexWriterConfig);
            indexWriter.deleteAll();
            for (File file : new File(CN_FILE_PATH).listFiles()) {
                document = new Document();
                document.add(new TextField("content", FileUtils.readFileToString(file, "UTF-8"), Field.Store.YES));
                document.add(new StringField("filePath", file.getAbsolutePath(), Field.Store.YES));
                indexWriter.addDocument(document);
            }
        } catch (Exception e) {
            System.out.println("创建索引的过程中遇到异常,堆栈轨迹如下");
            e.printStackTrace();
        } finally {
            try {
                if (null != indexWriter) {
                    indexWriter.close();
                }
            } catch (Exception e) {
                System.out.println("关闭IndexWriter时遇到异常,堆栈轨迹如下");
                e.printStackTrace();
            }
        }
    }

    public void createENIndex() {
        Directory directory = null;
        IndexWriter indexWriter = null;
        Document document = null;
        try {
            directory = FSDirectory.open(FileSystems.getDefault().getPath(INDEX_EN));
            Analyzer analyzer = new EnglishAnalyzer();
            IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(directory, indexWriterConfig);
            indexWriter.deleteAll();
            for (File file : new File(EN_FILE_PATH).listFiles()) {
                document = new Document();
                document.add(new TextField("content", FileUtils.readFileToString(file, "UTF-8"), Field.Store.YES));
                document.add(new StringField("filePath", file.getAbsolutePath(), Field.Store.YES));
                indexWriter.addDocument(document);
            }
        } catch (Exception e) {
            System.out.println("创建索引的过程中遇到异常,堆栈轨迹如下");
            e.printStackTrace();
        } finally {
            try {
                if (null != indexWriter) {
                    indexWriter.close();
                }
            } catch (Exception e) {
                System.out.println("关闭IndexWriter时遇到异常,堆栈轨迹如下");
                e.printStackTrace();
            }
        }
    }

    public void searchCNFile(String queryField) {
        searchResult.clear();
        IndexReader indexReader = null;
        try {
            //创建Directory
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath(INDEX_CN));
            //创建IndexReader
            indexReader = DirectoryReader.open(directory);
            //根据IndexReader创建IndexSearcher
            IndexSearcher indexSearcher = new IndexSearcher(indexReader);
            //创建用于搜索的Query
            QueryParser queryParser = new QueryParser("content", new SmartChineseAnalyzer());
            queryParser.setDefaultOperator(QueryParser.Operator.AND);
            Query query = queryParser.parse(queryField);
            /*根据Searcher返回TopDocs
             只显示前50条搜索结果
             */
            TopDocs topDocs = indexSearcher.search(query, 50);
            //获取ScoreDocs对象
            ScoreDoc[] scoreDocs = topDocs.scoreDocs;
            System.out.println("共找到搜索结果：" + topDocs.totalHits + "个");
            for (ScoreDoc scoreDoc : scoreDocs) {
                //scoreDoc.doc得到文档的序号
                Document document = indexSearcher.doc(scoreDoc.doc);
                searchResult.add(document.get("filePath"));
                System.out.println(document.get("filePath"));
            }
        } catch (Exception e) {
            System.out.println("搜索文件的过程中遇到异常,堆栈轨迹如下");
            e.printStackTrace();
        } finally {
            if (indexReader != null) {
                try {
                    indexReader.close();
                } catch (IOException e) {
                    System.out.println("关闭IndexReader时遇到异常,堆栈轨迹如下");
                    e.printStackTrace();
                }
            }
        }
    }

    public void searchENFile(String queryField) {
        searchResult.clear();
        IndexReader indexReader = null;
        try {
            //创建Directory
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath(INDEX_EN));
            //创建IndexReader
            indexReader = DirectoryReader.open(directory);
            //根据IndexReader创建IndexSearcher
            IndexSearcher indexSearcher = new IndexSearcher(indexReader);
            //创建用于搜索的Query
            QueryParser queryParser = new QueryParser("content", new EnglishAnalyzer());
            queryParser.setDefaultOperator(QueryParser.Operator.AND);
            Query query = queryParser.parse(queryField);
            /*根据Searcher返回TopDocs
             只显示前50条搜索结果
             */
            TopDocs topDocs = indexSearcher.search(query, 50);
            //获取ScoreDocs对象
            ScoreDoc[] scoreDocs = topDocs.scoreDocs;
            System.out.println("共找到搜索结果：" + topDocs.totalHits + "个");
            for (ScoreDoc scoreDoc : scoreDocs) {
                //scoreDoc.doc得到文档的序号
                Document document = indexSearcher.doc(scoreDoc.doc);
                searchResult.add(document.get("filePath"));
                System.out.println(document.get("filePath"));
            }
        } catch (Exception e) {
            System.out.println("搜索文件的过程中遇到异常,堆栈轨迹如下");
            e.printStackTrace();
        } finally {
            if (indexReader != null) {
                try {
                    indexReader.close();
                } catch (IOException e) {
                    System.out.println("关闭IndexReader时遇到异常,堆栈轨迹如下");
                    e.printStackTrace();
                }
            }
        }
    }

    public List<String> getSearchResult() {
        return searchResult;
    }
}
