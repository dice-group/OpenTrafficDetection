import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class ChangeClass {
	
	
	public static Set<String> allowedClasses = new LinkedHashSet<String>();

	public static void main(String[] args) throws IOException {

		String path = "/home/gsjunior/git/object_detection/training/train";
		//String path = args[0];
		String oldClass = "7";
		String newClass = "5";


		File filePath = new File(path);
		
		List<File> listFiles = listFilesForFolder(filePath);
		
		for(File file : listFiles) {
			System.out.println(file.getAbsolutePath());
			FileReader fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			
			List<String> newLines = new ArrayList<String>();
			
			String line;
			while ((line = br.readLine()) != null) {
                String[] s = line.split("\\s+");
                if(s[0].equals(oldClass)) {
                	StringBuilder newLine = new StringBuilder("");
                	newLine.append(newClass).append(" ");
                	newLine.append(s[1]).append(" ");
                	newLine.append(s[2]).append(" ");
                	newLine.append(s[3]).append(" ");
                	newLine.append(s[4]);
                	System.out.println(" --" + newLine.toString());
                	newLines.add(newLine.toString());
                }
            }
			
			if(!newLines.isEmpty()) {
			
				FileWriter fw = new FileWriter(file);
				BufferedWriter bw = new BufferedWriter(fw);
				for(String s : newLines) {
					bw.write(s);
					bw.newLine();
				}
				bw.close();
				br.close();
			}
		}
		
	}

	public static List<File> listFilesForFolder(final File folder) {
		List<File> listFiles = new ArrayList<File>();
		
		for (final File fileEntry : folder.listFiles()) {
			if(fileEntry.getName().endsWith("txt")) {
				listFiles.add(fileEntry);
			}
		}
		return listFiles;
	}
	

}
