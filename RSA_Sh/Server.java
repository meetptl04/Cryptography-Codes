import java.io.*;
import java.math.BigInteger;
import java.net.*;

public class Server {

  public static void main(String[] args) throws Exception {
    RSALibrary.fillPrimes();
    RSALibrary.generateKeys();
    System.out.println("Server's Public Key (e): " + RSALibrary.publicKey);
    System.out.println("Server's n: " + RSALibrary.n);

    ServerSocket serverSocket = new ServerSocket(9999);
    System.out.println("Server is listening...");

    Socket clientSocket = serverSocket.accept();
    System.out.println("Connected with " + clientSocket.getInetAddress());

    DataInputStream dis = new DataInputStream(clientSocket.getInputStream());
    PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

    String publicKeyInfo = RSALibrary.publicKey + " " + RSALibrary.n;
    System.out.println("Sending to client: " + publicKeyInfo);
    out.println(publicKeyInfo);

    String clientKeyInfo = dis.readLine();
    System.out.println("Received client key info: " + clientKeyInfo);
    String[] parts = clientKeyInfo.split("\\|");
    BigInteger clientE = new BigInteger(parts[0]);
    BigInteger clientN = new BigInteger(parts[1]);
    System.out.println("Client's Public Key (e): " + clientE);
    System.out.println("Client's n: " + clientN);

    String fileInfo = dis.readLine();
    System.out.println("Received file info: " + fileInfo);
    String[] fileParts = fileInfo.split("\\|");
    String fileName = fileParts[0];
    BigInteger signature = new BigInteger(fileParts[1]);
    System.out.println("File name: " + fileName);
    System.out.println("Signature: " + signature);

    FileOutputStream fos = new FileOutputStream(fileName);
    byte[] buffer = new byte[4096];
    int bytesRead;
    while ((bytesRead = clientSocket.getInputStream().read(buffer)) > 0) {
      System.out.println("Received file chunk: " + bytesRead + " bytes");
      fos.write(buffer, 0, bytesRead);
    }
    fos.close();

    byte[] fileData = java.nio.file.Files.readAllBytes(
      java.nio.file.Paths.get(fileName)
    );
    System.out.println(
      "File data read for verification: " + fileData.length + " bytes"
    );

    if (RSALibrary.verify(signature, fileData, clientE, clientN)) {
      System.out.println("File signature verified successfully.");
    } else {
      System.out.println("File signature verification failed.");
    }

    clientSocket.close();
    serverSocket.close();
    System.out.println("File received and connection closed.");
  }
}
