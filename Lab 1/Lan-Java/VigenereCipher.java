import java.util.Scanner;

public class VigenereCipher {

    public static String encrypt(String plaintext, String key) {
        StringBuilder ciphertext = new StringBuilder();
        int keyIndex = 0;

        for (int i = 0; i < plaintext.length(); i++) {
            char plaintextChar = plaintext.charAt(i);
            if (Character.isLetter(plaintextChar)) {
                char keyChar = key.charAt(keyIndex % key.length());
                int shift = Character.toUpperCase(keyChar) - 'A';
                
                if (Character.isUpperCase(plaintextChar)) {
                    char encryptedChar = (char) (((plaintextChar - 'A' + shift) % 26) + 'A');
                    ciphertext.append(encryptedChar);
                } else {
                    char encryptedChar = (char) (((plaintextChar - 'a' + shift) % 26) + 'a');
                    ciphertext.append(encryptedChar);
                }
                keyIndex++;
            } else {
                ciphertext.append(plaintextChar);
            }
        }
        return ciphertext.toString();
    }

    public static String decrypt(String ciphertext, String key) {
        StringBuilder plaintext = new StringBuilder();
        int keyIndex = 0;

        for (int i = 0; i < ciphertext.length(); i++) {
            char ciphertextChar = ciphertext.charAt(i);
            if (Character.isLetter(ciphertextChar)) {
                char keyChar = key.charAt(keyIndex % key.length());
                int shift = Character.toUpperCase(keyChar) - 'A';
                
                if (Character.isUpperCase(ciphertextChar)) {
                    char decryptedChar = (char) (((ciphertextChar - 'A' - shift + 26) % 26) + 'A');
                    plaintext.append(decryptedChar);
                } else {
                    char decryptedChar = (char) (((ciphertextChar - 'a' - shift + 26) % 26) + 'a');
                    plaintext.append(decryptedChar);
                }
                keyIndex++;
            } else {
                plaintext.append(ciphertextChar);
            }
        }
        return plaintext.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Vigenère Cipher");
        System.out.println("Choose an option:");
        System.out.println("1. Encrypt");
        System.out.println("2. Decrypt");
        int choice = sc.nextInt();
        sc.nextLine();

        System.out.print("Enter the key: ");
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
