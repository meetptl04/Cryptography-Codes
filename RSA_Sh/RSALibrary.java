import java.math.BigInteger;
import java.security.MessageDigest;
import java.util.*;

public class RSALibrary {

  private static Set<Integer> primes = new HashSet<>();
  public static BigInteger publicKey, privateKey, n;

  public static void fillPrimes() {
    boolean[] sieve = new boolean[250];
    Arrays.fill(sieve, true);
    sieve[0] = sieve[1] = false;
    for (int i = 2; i < sieve.length; i++) {
      if (sieve[i]) {
        for (int j = i * 2; j < sieve.length; j += i) {
          sieve[j] = false;
        }
      }
    }
    for (int i = 0; i < sieve.length; i++) {
      if (sieve[i]) primes.add(i);
    }
  }

  private static int getRandomPrime() {
    List<Integer> primeList = new ArrayList<>(primes);
    int idx = new Random().nextInt(primeList.size());
    int prime = primeList.get(idx);
    primes.remove(prime);
    return prime;
  }

  public static void generateKeys() {
    int p = getRandomPrime();
    int q = getRandomPrime();
    n = BigInteger.valueOf(p).multiply(BigInteger.valueOf(q));
    BigInteger fi = BigInteger
      .valueOf(p - 1)
      .multiply(BigInteger.valueOf(q - 1));

    BigInteger e = BigInteger.valueOf(2);
    while (e.gcd(fi).compareTo(BigInteger.ONE) != 0) {
      e = e.add(BigInteger.ONE);
    }
    publicKey = e;
    privateKey = e.modInverse(fi);

    System.out.println("Private Key (d): " + privateKey);
    System.out.println("Prime1: " + p);
    System.out.println("Prime2: " + q);
    System.out.println("Public Key (e): " + publicKey);
    System.out.println("n: " + n);
    System.out.println("Euler's Totient (fi): " + fi);
  }

  public static BigInteger secureHash(byte[] data, BigInteger mod)
    throws Exception {
    MessageDigest digest = MessageDigest.getInstance("SHA-512");
    byte[] hashBytes = digest.digest(data);
    System.out.println("Full SHA512 Hash: " + bytesToHex(hashBytes));
    BigInteger hashValue = new BigInteger(1, hashBytes);
    return hashValue.mod(mod);
  }

  public static BigInteger sign(byte[] data) throws Exception {
    BigInteger hash = secureHash(data, n);
    System.out.println("Computed SHA512 digest (mod n) for signing: " + hash);
    return hash.modPow(privateKey, n);
  }

  public static boolean verify(
    BigInteger signature,
    byte[] data,
    BigInteger pubKey,
    BigInteger modulus
  ) throws Exception {
    BigInteger hash = secureHash(data, modulus);
    System.out.println(
      "Computed SHA512 digest (mod n) for verification: " + hash
    );
    BigInteger recovered = signature.modPow(pubKey, modulus);
    System.out.println("Recovered hash from signature: " + recovered);
    return recovered.equals(hash);
  }

  private static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
      sb.append(String.format("%02x", b));
    }
    return sb.toString();
  }
}
