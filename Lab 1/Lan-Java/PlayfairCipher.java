import java.util.Scanner;

public class PlayfairCipher {

    private static char[][] keyMatrix = new char[5][5];

    public static void generateKeyMatrix(String key) {
        boolean[] used = new boolean[26];
        key = key.toUpperCase().replaceAll("[J]", "I");
        StringBuilder keyBuilder = new StringBuilder();

        for (char c : key.toCharArray()) {
            if (Character.isLetter(c) && !used[c - 'A']) {
                keyBuilder.append(c);
                used[c - 'A'] = true;
            }
        }

        for (char c = 'A'; c <= 'Z'; c++) {
            if (c != 'J' && !used[c - 'A']) {
                keyBuilder.append(c);
            }
        }

        String keyString = keyBuilder.toString();
        for (int i = 0; i < 25; i++) {
            keyMatrix[i / 5][i % 5] = keyString.charAt(i);
        }
    }

    public static String encrypt(String plaintext) {
        plaintext = prepareText(plaintext.toUpperCase().replaceAll("[J]", "I"));
        StringBuilder ciphertext = new StringBuilder();

        for (int i = 0; i < plaintext.length(); i += 2) {
            char a = plaintext.charAt(i);
            char b = plaintext.charAt(i + 1);
            int[] posA = findPosition(a);
            int[] posB = findPosition(b);

            if (posA[0] == posB[0]) {
                ciphertext.append(keyMatrix[posA[0]][(posA[1] + 1) % 5]);
                ciphertext.append(keyMatrix[posB[0]][(posB[1] + 1) % 5]);
            } else if (posA[1] == posB[1]) {
                ciphertext.append(keyMatrix[(posA[0] + 1) % 5][posA[1]]);
                ciphertext.append(keyMatrix[(posB[0] + 1) % 5][posB[1]]);
            } else {
                ciphertext.append(keyMatrix[posA[0]][posB[1]]);
                ciphertext.append(keyMatrix[posB[0]][posA[1]]);
            }
        }
        return ciphertext.toString();
    }

    public static String decrypt(String ciphertext) {
        StringBuilder plaintext = new StringBuilder();

        for (int i = 0; i < ciphertext.length(); i += 2) {
            char a = ciphertext.charAt(i);
            char b = ciphertext.charAt(i + 1);
            int[] posA = findPosition(a);
            int[] posB = findPosition(b);

            if (posA[0] == posB[0]) {
                plaintext.append(keyMatrix[posA[0]][(posA[1] + 4) % 5]);
                plaintext.append(keyMatrix[posB[0]][(posB[1] + 4) % 5]);
            } else if (posA[1] == posB[1]) {
                plaintext.append(keyMatrix[(posA[0] + 4) % 5][posA[1]]);
                plaintext.append(keyMatrix[(posB[0] + 4) % 5][posB[1]]);
            } else {
                plaintext.append(keyMatrix[posA[0]][posB[1]]);
                plaintext.append(keyMatrix[posB[0]][posA[1]]);
            }
        }
        return plaintext.toString().replace("X", "");
    }

    private static String prepareText(String text) {
        text = text.replaceAll("[^A-Z]", "");
        StringBuilder result = new StringBuilder();

        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (i + 1 < text.length() && c == text.charAt(i + 1)) {
                result.append(c).append('X');
            } else {
                result.append(c);
            }
        }
        if (result.length() % 2 != 0) {
            result.append('X');
        }
        return result.toString();
    }

    private static int[] findPosition(char c) {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (keyMatrix[i][j] == c) {
                    return new int[]{i, j};
                }
            }
        }
        return null;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the key for the Playfair Cipher:");
        String key = sc.nextLine();
        generateKeyMatrix(key);

        System.out.println("Select an option:");
        System.out.println("1. Encrypt a message");
        System.out.println("2. Decrypt a message");
        int choice = sc.nextInt();
        sc.nextLine();

        if (choice == 1) {
            System.out.println("Enter the plaintext:");
            String plaintext = sc.nextLine();
            String ciphertext = encrypt(plaintext);
            System.out.println("Ciphertext: " + ciphertext);
        } else if (choice == 2) {
            System.out.println("Enter the ciphertext:");
            String ciphertext = sc.nextLine();
            String plaintext = decrypt(ciphertext);
            System.out.println("Plaintext: " + plaintext);
        } else {
            System.out.println("Invalid option. Please select 1 or 2.");
        }

        sc.close();
    }
}
