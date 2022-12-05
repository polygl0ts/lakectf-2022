package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"io"
	"math/big"
	"os"
	"time"

	"github.com/ProtonMail/go-crypto/openpgp/armor"

	"github.com/ProtonMail/go-crypto/openpgp"
	"github.com/ProtonMail/go-crypto/openpgp/packet"
)

func main() {
	key, err := rsa.GenerateKey(rand.Reader, 4096)
	if err != nil {
		panic("Cannot generate RSA key")
	}
	subKey, err := rsa.GenerateKey(rand.Reader, 4096)
	if err != nil {
		panic("Cannot generate RSA key")
	}

	gpgKey := createPgpFromRsa(key, subKey, "epfl-ctf-admin@protonmail.com")
	writePrivateKey(gpgKey, "key1-pub.asc", false)
	writePrivateKey(gpgKey, "key1-sec.asc", true)

	keyFactor := key.Primes[0]
	subKeyFactor := subKey.Primes[0]
	key, err = generateKeyWithPrimeFactor(rand.Reader, keyFactor, 4096)
	if err != nil {
		panic("Cannot generate RSA key with common factor")
	}
	subKey, err = generateKeyWithPrimeFactor(rand.Reader, subKeyFactor, 4096)
	if err != nil {
		panic("Cannot generate RSA key with common factor")
	}

	gpgKey = createPgpFromRsa(key, subKey, "epfl-ctf-admin2@protonmail.com")
	writePrivateKey(gpgKey, "key2-pub.asc", false)
	writePrivateKey(gpgKey, "key2-sec.asc", true)
}

func createPgpFromRsa(key *rsa.PrivateKey, subKey *rsa.PrivateKey, email string) *openpgp.Entity {
	location, _ := time.LoadLocation("Europe/Zurich")
	creationTime := time.Date(2022, 6, 1, 13, 37, 0, 0, location)

	gpgKey := &openpgp.Entity{
		PrimaryKey: packet.NewRSAPublicKey(creationTime, &key.PublicKey),
		PrivateKey: packet.NewRSAPrivateKey(creationTime, key),
		Identities: make(map[string]*openpgp.Identity),
	}
	uid := packet.NewUserId(email, "", email)
	isPrimaryID := true
	gpgKey.Identities[uid.Id] = &openpgp.Identity{
		Name:   uid.Id,
		UserId: uid,
		SelfSignature: &packet.Signature{
			CreationTime:              creationTime,
			SigType:                   packet.SigTypeGenericCert,
			PubKeyAlgo:                packet.PubKeyAlgoRSA,
			Hash:                      crypto.SHA256,
			IsPrimaryId:               &isPrimaryID,
			FlagsValid:                true,
			FlagSign:                  true,
			FlagCertify:               true,
			FlagEncryptStorage:        true,
			FlagEncryptCommunications: true,
			IssuerKeyId:               &gpgKey.PrimaryKey.KeyId,
			PreferredSymmetric:        []uint8{uint8(packet.CipherAES256), uint8(packet.CipherAES128), uint8(packet.CipherAES192), uint8(packet.CipherCAST5), uint8(packet.Cipher3DES)},
			PreferredHash:             []uint8{8, 10, 2},
			PreferredCompression:      []uint8{uint8(packet.CompressionZLIB), uint8(packet.CompressionZIP), uint8(packet.CompressionNone)},
		},
	}
	err := gpgKey.Identities[uid.Id].SelfSignature.SignUserId(uid.Id, gpgKey.PrimaryKey, gpgKey.PrivateKey, nil)
	if err != nil {
		panic(err)
	}

	subkey := openpgp.Subkey{
		PublicKey:  packet.NewRSAPublicKey(creationTime, &subKey.PublicKey),
		PrivateKey: packet.NewRSAPrivateKey(creationTime, subKey),
		Sig: &packet.Signature{
			CreationTime:              creationTime,
			SigType:                   packet.SigTypeSubkeyBinding,
			PubKeyAlgo:                packet.PubKeyAlgoRSA,
			Hash:                      crypto.SHA256,
			FlagsValid:                true,
			FlagEncryptStorage:        true,
			FlagEncryptCommunications: true,
			IssuerKeyId:               &gpgKey.PrimaryKey.KeyId,
		},
	}

	subkey.PublicKey.IsSubkey = true
	subkey.PrivateKey.IsSubkey = true
	subkey.Sig.SignKey(subkey.PublicKey, gpgKey.PrivateKey, nil)

	gpgKey.Subkeys = append(gpgKey.Subkeys, subkey)

	return gpgKey
}

func writePrivateKey(gpgKey *openpgp.Entity, filename string, private bool) {
	var writer io.WriteCloser
	writer, err := os.Create(filename)
	if err != nil {
		panic(err)
	}

	keyType := openpgp.PublicKeyType
	if private {
		keyType = openpgp.PrivateKeyType
	}
	writer, err = armor.Encode(writer, keyType, make(map[string]string))
	if err != nil {
		panic(err)
	}

	if private {
		err = gpgKey.SerializePrivate(writer, nil)
	} else {
		err = gpgKey.Serialize(writer)
	}
	if err != nil {
		panic(err)
	}
	err = writer.Close()
	if err != nil {
		panic(err)
	}
}

func generateKeyWithPrimeFactor(random io.Reader, primeFactor *big.Int, bits int) (*rsa.PrivateKey, error) {
	var bigOne = big.NewInt(1)
	priv := new(rsa.PrivateKey)
	priv.E = 65537

	primes := make([]*big.Int, 2)
	primes[0] = primeFactor

	for {
		todo := bits - primes[0].BitLen()

		var err error
		primes[1], err = rand.Prime(random, todo)
		if err != nil {
			return nil, err
		}
		todo -= primes[1].BitLen()

		// Make sure that primes are not equal.
		if primes[0].Cmp(primes[1]) == 0 {
			continue
		}

		n := new(big.Int).Set(bigOne)
		totient := new(big.Int).Set(bigOne)
		pminus1 := new(big.Int)
		for _, prime := range primes {
			n.Mul(n, prime)
			pminus1.Sub(prime, bigOne)
			totient.Mul(totient, pminus1)
		}

		if n.BitLen() != bits {
			// This should never happen for nprimes == 2 because
			// crypto/rand should set the top two bits in each prime.
			// For nprimes > 2 we hope it does not happen often.
			continue
		}

		priv.D = new(big.Int)
		e := big.NewInt(int64(priv.E))
		ok := priv.D.ModInverse(e, totient)

		if ok != nil {
			priv.Primes = primes
			priv.N = n
			break
		}
	}

	priv.Precompute()
	return priv, nil
}
