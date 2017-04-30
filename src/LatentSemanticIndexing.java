// LatentSemanticIndexing.java

// TODO: Get Lucene packages
// TODO: Get sample code below running
// TODO: Adapt code for sample task NL query among code base

import org.apache.lucene.analysis.standard.StandardAnalyzer;
//import org.apache.lucene.queryparser.classic.*;
import org.apache.lucene.queryparser.classic.QueryParserBase;
import org.apache.lucene.util.QueryBuilder;
import org.apache.lucene.document.*;
import org.apache.lucene.analysis.*;
import org.apache.lucene.search.*;
import org.apache.lucene.index.*;
import org.apache.lucene.store.*;

public class LatentSemanticIndexing {

  // Main method: called from command line
  public static void main(String args[]) {

    Analyzer analyzer = new StandardAnalyzer();

    // Store the index in memory:
    Directory directory = new RAMDirectory();

    // To store an index on disk, use this instead:
    //Directory directory = FSDirectory.open("/tmp/testindex");
    IndexWriterConfig config = new IndexWriterConfig(analyzer);
    IndexWriter iwriter = new IndexWriter(directory, config);
    Document doc = new Document();
    String text = "This is the text to be indexed.";
    doc.add(new Field("fieldname", text, TextField.TYPE_STORED));
    iwriter.addDocument(doc);
    iwriter.close();

    // Now search the index:
    DirectoryReader ireader = DirectoryReader.open(directory);
    IndexSearcher isearcher = new IndexSearcher(ireader);
    // Parse a simple query that searches for "text":
    QueryParser parser = new QueryParser("fieldname", analyzer);
    Query query = parser.parse("text");
    ScoreDoc[] hits = isearcher.search(query, null, 1000).scoreDocs;
 //   assertEquals(1, hits.length);
    // Iterate through the results:
    for (int i = 0; i < hits.length; i++) {
      Document hitDoc = isearcher.doc(hits[i].doc);
  //    assertEquals("This is the text to be indexed.", hitDoc.get("fieldname"));
    }

    ireader.close();
    directory.close();
  }
}
