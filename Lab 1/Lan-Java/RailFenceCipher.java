import java.util.Scanner;

public class RailFenceCipher {

    public static String encrypt(String plaintext, int numRails) {
        char[][] rail = new char[numRails][plaintext.length()];
        for (int i = 0; i < numRails; i++) {
            for (int j = 0; j < plaintext.length(); j++) {
                rail[i][j] = '\n';
            }
        }

        int row = 0;
        boolean down = true;
        for (int i = 0; i < plaintext.length(); i++) {
            rail[row][i] = plaintext.charAt(i);
            if (row == 0) {
                down = true;
            }
            if (row == numRails - 1) {
                down = false;
            }
            row = down ? row + 1 : row - 1;
        }

        StringBuilder ciphertext = new StringBuilder();
        for (int i = 0; i < numRails; i++) {
            for (int j = 0; j < plaintext.length(); j++) {
                if (rail[i][j] != '\n') {
                    ciphertext.append(rail[i][j]);
                }
            }
        }
        return ciphertext.toString();
    }

    public static String decrypt(String ciphertext, int numRails) {
        char[][] rail = new char[numRails][ciphertext.length()];
        for (int i = 0; i < numRails; i++) {
            for (int j = 0; j < ciphertext.length(); j++) {
                rail[i][j] = '\n';
            }
        }

        int row = 0;
        boolean down = true;
        for (int i = 0; i < ciphertext.length(); i++) {
            rail[row][i] = '*';
            if (row == 0) {
                down = true;
            }
            if (row == numRails - 1) {
                down = false;
            }
            row = down ? row + 1 : row - 1;
        }

        int index = 0;
        for (int i = 0; i < numRails; i++) {
            for (int j = 0; j < ciphertext.length(); j++) {
                if (rail[i][j] == '*' && index < ciphertext.length()) {
                    rail[i][j] = ciphertext.charAt(index++);
                }
            }
        }

        StringBuilder plaintext = new StringBuilder();
        row = 0;
        down = true;
        for (int i = 0; i < ciphertext.length(); i++) {
            plaintext.append(rail[row][i]);
            if (row == 0) {
                down = true;
            }
            if (row == numRails - 1) {
                down = false;
            }
            row = down ? row + 1 : row - 1;
        }
        return plaintext.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Rail Fence Cipher");
        System.out.println("Choose an option:");
        System.out.println("1. Encrypt");
        System.out.println("2. Decrypt");
        int choice = sc.nextInt();
        sc.nextLine();

        System.out.print("Enter the number of rails: ");
        int numRails = sc.nextInt();
        sc.nextLine();

        if (choice == 1) {
            System.out.print("Enter the plaintext: ");
            String plaintext = sc.nextLine();
            String ciphertext = encrypt(plaintext, numRails);
            System.out.println("Encrypted text: " + ciphertext);
        } else if (choice == 2) {
            System.out.print("Enter the ciphertext: ");
            String ciphertext = sc.nextLine();
            String decryptedText = decrypt(ciphertext, numRails);
            System.out.println("Decrypted text: " + decryptedText);
        } else {
            System.out.println("Invalid choice.");
        }

        sc.close();
    }
}
