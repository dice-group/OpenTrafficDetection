import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class FilterClass {
	
	public static Set<String> allowedClasses = new LinkedHashSet<String>();

	public static void main(String[] args) throws IOException {
		
		allowedClasses.add("0"); //person
		//allowedClasses.add("1"); //bicycle
		allowedClasses.add("2"); //car
		allowedClasses.add("3"); //motorbike
		allowedClasses.add("5"); //bus
		//allowedClasses.add("6"); //train
		allowedClasses.add("7"); //truck
		//allowedClasses.add("15"); //cat
		//allowedClasses.add("16"); //dog
		

		String pathVal = "/home/gsjunior/git/object_detection/training/coco/labels/val2014";
		String imgVal = "/home/gsjunior/git/object_detection/training/coco/images/val2014/";
		String destFolder = "/home/gsjunior/git/object_detection/training/test/";

		//String path = args[0];
		


		File filePath = new File(pathVal);
		
		List<File> listFiles = listFilesForFolder(filePath);
		
		for(File file : listFiles) {
			System.out.println(file.getAbsolutePath());
			FileReader fr = new FileReader(file);
			BufferedReader br = new BufferedReader(fr);
			
			String line;
			boolean contains = false;
			List<String> lines = new ArrayList<String>();
			while ((line = br.readLine()) != null) {
                String[] s = line.split("\\s+");
                
                if(allowedClasses.contains(s[0])) {
                	contains = true;
                	StringBuilder newLine = new StringBuilder("");
                	newLine.append(s[0]).append(" ");
                	newLine.append(s[1]).append(" ");
                	newLine.append(s[2]).append(" ");
                	newLine.append(s[3]).append(" ");
                	newLine.append(s[4]);
                	System.out.println(" --" + newLine.toString());
                	lines.add(newLine.toString());
                }
                
            }
			
			
			if(contains) {
				
				Path originalPath = Paths.get(imgVal + file.getName().replaceAll("txt","jpg"));
				Path imgCopied = Paths.get(destFolder + file.getName().replaceAll("txt","jpg"));
				Files.copy(originalPath, imgCopied, StandardCopyOption.REPLACE_EXISTING);
				FileWriter fw = new FileWriter(new File(destFolder + file.getName()));
				BufferedWriter bw = new BufferedWriter(fw);
				
				for(String s : lines) {
					bw.write(s);
					bw.newLine();
				}
				bw.close();
			}
				
			
			br.close();
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
