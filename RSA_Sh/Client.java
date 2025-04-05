import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.util.Scanner;

public class Client {

  public static void main(String[] args) throws Exception {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the file name to send: ");
    String fileName = scanner.nextLine();
    System.out.println("File to send: " + fileName);

    Socket socket = new Socket("localhost", 9999);
    System.out.println("Client connected to server.");

    DataInputStream dis = new DataInputStream(socket.getInputStream());
    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

    String publicKeyInfo = dis.readLine();
    System.out.println("Received from server: " + publicKeyInfo);
    String[] parts = publicKeyInfo.split(" ");
    BigInteger num1 = new BigInteger(parts[0]);
    BigInteger num2 = new BigInteger(parts[1]);
    System.out.println("Server's Public Key (e, n): " + num1 + ", " + num2);

    RSALibrary.fillPrimes();
    RSALibrary.generateKeys();

    String clientKeyInfo = RSALibrary.publicKey + "|" + RSALibrary.n;
    System.out.println(
      "Sending client's public key to server: " + clientKeyInfo
    );
    out.println(clientKeyInfo);

    byte[] fileData = java.nio.file.Files.readAllBytes(
      java.nio.file.Paths.get(fileName)
    );
    System.out.println("File data read: " + fileData.length + " bytes");

    BigInteger signature = RSALibrary.sign(fileData);
    System.out.println("File signature: " + signature);

    String fileInfo = fileName + "|" + signature;
    System.out.println("Sending file info to server: " + fileInfo);
    out.println(fileInfo);

    OutputStream os = socket.getOutputStream();
    int chunkSize = 4096;
    for (int i = 0; i < fileData.length; i += chunkSize) {
      int end = Math.min(fileData.length, i + chunkSize);
      os.write(fileData, i, end - i);
      System.out.println("Sending file chunk: " + (end - i) + " bytes");
    }
    os.flush();

    System.out.println("File sent to server.");
    socket.close();
    scanner.close();
  }
}
