import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;

import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException, CsvValidationException {
        String fileName = "kM.csv";
        FileReader filereader = new FileReader(fileName);
        CSVReader csvReader = new CSVReader(filereader);
        String[] nextRecord;
        int stt = 0;
        while ((nextRecord = csvReader.readNext()) != null) {
//            for (String cell : nextRecord) {
//                System.out.print(cell + "\t");
//            }
            File sum = new File(  "C:\\CODE\\Hethongthongminh\\Evaluation\\rouge2_v1.2.2_runnable\\v1.2.2\\test-summarization-kM\\reference\\" + stt + "_kM.txt");
            File content = new File("C:\\CODE\\Hethongthongminh\\Evaluation\\rouge2_v1.2.2_runnable\\v1.2.2\\test-summarization-kM\\system\\" + stt + "_kM.txt");
            FileWriter writerSum = new FileWriter(sum);
            PrintWriter printWriter1 = new PrintWriter(writerSum);
            FileWriter writerContent = new FileWriter(content);
            PrintWriter printWriter2 = new PrintWriter(writerContent);
            if (!sum.exists())
                sum.createNewFile();
            if(!content.exists())
                content.createNewFile();
//            if(nextRecord[0].length()>12) {
//                printWriter1.println(nextRecord[0].substring(12));
////                System.out.println(stt);
//            }
            if(!nextRecord[2].equals("system"))
                printWriter1.println(nextRecord[2]);


            if(!nextRecord[1].equals("reference"))
                printWriter2.println(nextRecord[1]);
            stt++;
            System.out.println(stt);

            printWriter1.close();
            printWriter2.close();
        }
    }
}
