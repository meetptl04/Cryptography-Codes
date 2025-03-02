import java.util.Scanner;

public class RowTranspositionCipher {

    public static String encrypt(String plaintext, String key) {
        int rows = (int) Math.ceil((double) plaintext.length() / key.length());
        char[][] grid = new char[rows][key.length()];
        int index = 0;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < key.length(); j++) {
                if (index < plaintext.length()) {
                    grid[i][j] = plaintext.charAt(index++);
                } else {
                    grid[i][j] = 'X';
                }
            }
        }

        StringBuilder ciphertext = new StringBuilder();
        for (int i = 0; i < key.length(); i++) {
            int column = key.charAt(i) - '0';
            for (int j = 0; j < rows; j++) {
                ciphertext.append(grid[j][column]);
            }
        }

        return ciphertext.toString();
    }

    public static String decrypt(String ciphertext, String key) {
        int rows = (int) Math.ceil((double) ciphertext.length() / key.length());
        int columns = key.length();
        char[][] grid = new char[rows][columns];
        int index = 0;

        StringBuilder plaintext = new StringBuilder();
        for (int i = 0; i < columns; i++) {
            int column = key.charAt(i) - '0';
            for (int j = 0; j < rows; j++) {
                grid[j][column] = ciphertext.charAt(index++);
            }
        }

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                if (grid[i][j] != 'X') {
                    plaintext.append(grid[i][j]);
                }
            }
        }

        return plaintext.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Row Transposition Cipher");
        System.out.println("Choose an option:");
        System.out.println("1. Encrypt");
        System.out.println("2. Decrypt");
        int choice = sc.nextInt();
        sc.nextLine();

        System.out.print("Enter the key (numeric string): ");
        String key = sc.nextLine();

        if (choice == 1) {
            System.out.print("Enter the plaintext: ");
            String plaintext = sc.nextLine();
            String ciphertext = encrypt(plaintext, key);
            System.out.println("Encrypted text: " + ciphertext);
        } else if (choice == 2) {
            System.out.print("Enter the ciphertext: ");
            String ciphertext = sc.nextLine();
            String decryptedText = decrypt(ciphertext, key);
            System.out.println("Decrypted text: " + decryptedText);
        } else {
            System.out.println("Invalid choice.");
        }

        sc.close();
    }
}
