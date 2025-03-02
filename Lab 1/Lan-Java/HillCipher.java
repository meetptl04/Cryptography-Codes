import java.util.Scanner;

public class HillCipher {

    static void getKeyMatrix(String key, int keyMatrix[][]) {
        int k = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                keyMatrix[i][j] = (key.charAt(k)) % 65;
                k++;
            }
        }
    }

    static void encrypt(int cipherMatrix[][], int keyMatrix[][], int messageVector[][]) {
        for (int i = 0; i < 3; i++) {
            cipherMatrix[i][0] = 0;
            for (int j = 0; j < 3; j++) {
                cipherMatrix[i][0] += keyMatrix[i][j] * messageVector[j][0];
            }
            cipherMatrix[i][0] = cipherMatrix[i][0] % 26;
        }
    }

    static void HillCipher(String message, String key) {
        int[][] keyMatrix = new int[3][3];
        getKeyMatrix(key, keyMatrix);

        int[][] messageVector = new int[3][1];
        for (int i = 0; i < 3; i++)
            messageVector[i][0] = (message.charAt(i)) % 65;

        int[][] cipherMatrix = new int[3][1];
        encrypt(cipherMatrix, keyMatrix, messageVector);

        StringBuilder cipherText = new StringBuilder();
        for (int i = 0; i < 3; i++)
            cipherText.append((char) (cipherMatrix[i][0] + 65));

        System.out.println("Ciphertext: " + cipherText);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter the message (3 characters): ");
        String message = sc.nextLine().toUpperCase();

        System.out.print("Enter the key (9 characters): ");
        String key = sc.nextLine().toUpperCase();

        HillCipher(message, key);
        sc.close();
    }
}
