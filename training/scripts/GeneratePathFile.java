import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class GeneratePathFile {
	
	private static final String path = "/home/gsjunior/git/object_detection/training/train";
	
	
	public static void main(String[] args) throws IOException {
				
		List<File> listFiles = listFilesForFolder(new File(path));
		
		FileWriter fw = new FileWriter(new File("/home/gsjunior/git/object_detection/training/train.txt"));
		BufferedWriter bw = new BufferedWriter(fw);
		
		for(File file: listFiles) {
			String txtFile = file.getName().substring(0,file.getName().indexOf(".")) + ".txt";
			String txtFilePath = file.getAbsolutePath().substring(0,file.getAbsolutePath().lastIndexOf("/")+1) + txtFile;
			File yoloFile = new File(txtFilePath);
			//System.out.println(" File >> " + file.getAbsolutePath());
			if(!yoloFile.exists()) {
				System.out.println(yoloFile.getName());
				
				//bw.write(file.getAbsolutePath());
				//bw.newLine();
			}
		}
		bw.close();
	}
	
	public static List<File> listFilesForFolder(final File folder) {
		List<File> listFiles = new ArrayList<File>();
		
		for (final File fileEntry : folder.listFiles()) {
			if(fileEntry.getName().endsWith("jpeg") || fileEntry.getName().endsWith("jpg")) {
				listFiles.add(fileEntry);
			}
		}
		return listFiles;
	}

}
