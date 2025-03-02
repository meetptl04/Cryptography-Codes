import java.util.Scanner;

public class CaesarCipher {
    public static String encrypt(String text, int shift) {
        StringBuilder result = new StringBuilder();
        for (char character : text.toCharArray()) {
            if (Character.isLetter(character)) {
                char base = Character.isLowerCase(character) ? 'a' : 'A';
                result.append((char) ((character - base + shift) % 26 + base));
            } else {
                result.append(character);
            }
        }
        return result.toString();
    }

    public static String decrypt(String cipher, int shift) {
        StringBuilder result = new StringBuilder();
        for (char character : cipher.toCharArray()) {
            if (Character.isLetter(character)) {
                char base = Character.isLowerCase(character) ? 'a' : 'A';
                result.append((char) ((character - base - shift + 26) % 26 + base));
            } else {
                result.append(character);
            }
        }
        return result.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int shift = 3;

        System.out.println("Select an option:");
        System.out.println("1. Encrypt a message");
        System.out.println("2. Decrypt a message");
        int choice = sc.nextInt();
        sc.nextLine();

        if (choice == 1) {
            System.out.println("Enter the text to be encrypted:");
            String text = sc.nextLine();
            String encrypted = encrypt(text, shift);
            System.out.println("Encrypted Text: " + encrypted);
        } else if (choice == 2) {
            System.out.println("Enter the text to be decrypted:");
            String cipher = sc.nextLine();
            String decrypted = decrypt(cipher, shift);
            System.out.println("Decrypted Text: " + decrypted);
        } else {
            System.out.println("Invalid option. Please select 1 or 2.");
        }

        sc.close();
    }
}
