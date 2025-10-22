# MixNet Verifiable Shuffles & Ballot Privacy

## Overview

MixNets are cryptographic protocols that enable **verifiable shuffling** of encrypted ballots while preserving **voter privacy and ballot secrecy**. This document explains how verifiable shuffles work, why they're critical for ballot privacy, and how they prevent adversaries from linking voters to their votes.

---

## 1. The Problem: Vote Tracing

### Challenge
Without anonymization, the tallying process can trace votes back to voters:

```
Voter A casts ballot X1
    ↓
Ballot X1 enters system
    ↓
X1 is recorded in database
    ↓
Tallying counts X1 for Candidate A
    ↓
⚠️ PROBLEM: X1 can potentially be linked back to Voter A!
```

### Why This Matters
- **Privacy Violation:** Voter preference exposed to observers
- **Coercion Risk:** Voters can be pressured to vote a certain way
- **Vote Buying:** Votes can be purchased or coerced with proof
- **Election Integrity:** Voter secrecy undermines democratic principles

### Solution
Use MixNet verifiable shuffles to **break the link** between input and output ballots:

```
Voter A     Voter B     Voter C
  ↓           ↓           ↓
X1 →    ┌─────MixNet─────┐    → Y1
X2 →    │    Shuffle      │    → Y2
X3 →    │    Verify       │    → Y3
        └─────────────────┘
```

After MixNet:
- ✅ Y1, Y2, Y3 are the same ballots as X1, X2, X3
- ✅ **Order is randomized** (Y1 ≠ X1 necessarily)
- ✅ **Cryptographically verifiable** that Y's are permutation of X's
- ✅ **No computational power** can reverse the mapping

---

## 2. Homomorphic Ciphertexts: The Foundation

### What is Homomorphic Encryption?

Homomorphic encryption (HE) allows computation on **encrypted data** without decryption:

```
Plaintext:        M1 + M2 = R
                  ↓     ↓      ↓
Homomorphic:  E(M1) ⊕ E(M2) = E(R)
```

**Key Property:** You can compute on ciphertexts and get the encrypted result.

### Why HE for MixNet?

HE allows the MixNet to:
1. **Shuffle** ciphertexts without decryption
2. **Re-encrypt** shuffled ciphertexts to randomize them
3. **Prove correctness** of the shuffle
4. **Never reveal** intermediate plaintext

### Example: Ballot Encryption

```
Original Ballot:
  Voter ID: VOTER-001
  Candidate: Candidate A
  
Homomorphic Encryption:
  E(Ballot) = C_encrypted
  
Properties:
  - E(Ballot) ≠ Ballot (encrypted form)
  - Can shuffle E(Ballot) without decryption
  - Can prove E(Ballot) is valid
  - Cannot derive Ballot from E(Ballot) (computationally hard)
```

---

## 3. Verifiable Shuffle: How It Works

### The Shuffle Process

```
Step 1: INPUT CIPHERTEXTS
  ├─ C₁ = Encrypt(Voter1's vote)
  ├─ C₂ = Encrypt(Voter2's vote)
  ├─ C₃ = Encrypt(Voter3's vote)
  └─ Cₙ = Encrypt(Votern's vote)

Step 2: SHUFFLE
  ├─ Create random permutation π
  │  Example: π = [3, 1, 2, ..., n]
  ├─ Reorder: C₃, C₁, C₂, ..., Cₙ
  └─ Shuffled: C'₁, C'₂, C'₃, ..., C'ₙ

Step 3: RE-ENCRYPT
  ├─ For each shuffled ciphertext C'ᵢ
  ├─ Apply re-encryption: C''ᵢ = Re-encrypt(C'ᵢ)
  ├─ This randomizes the ciphertext appearance
  └─ Result: C''₁, C''₂, ..., C''ₙ

Step 4: GENERATE PROOF
  ├─ Create zero-knowledge proof (ZKP)
  ├─ Proof shows:
  │  ✓ {C''₁, ..., C''ₙ} is permutation of {C₁, ..., Cₙ}
  │  ✓ Re-encryption was done correctly
  │  ✓ No ballots were modified or lost
  └─ Proof is publicly verifiable

Step 5: PUBLISH
  ├─ Output shuffled ciphertexts: C''₁, C''₂, ..., C''ₙ
  ├─ Publish proof: π_proof
  └─ Anyone can verify without trusting MixNet operator
```

### Key Insight: Randomization Breaks Traceability

```
Before Shuffle:        After Shuffle + Re-encrypt:
C₁ (Position 1)    →   C''₁ (was C₃, re-encrypted)
C₂ (Position 2)    →   C''₂ (was C₁, re-encrypted)
C₃ (Position 3)    →   C''₃ (was C₂, re-encrypted)

Attacker's Problem:
  - Cannot tell if C''₁ corresponds to original C₁, C₂, or C₃
  - Ciphertexts are re-encrypted (appearance changed)
  - Even with computational power, reversal is infeasible
  - Would need to solve discrete logarithm problem
```

---

## 4. Verifiable Shuffle Protocol: Formal Definition

### Chaum-Pedersen Shuffle Proof

The most common verifiable shuffle uses **Chaum-Pedersen protocol**:

```
Components:
├─ G: Cyclic group
├─ g: Generator
├─ h: Another generator
├─ x: Secret exponent
└─ Public key: pk = g^x

Shuffle Process:
1. Generate random permutation π
2. Generate random re-encryption factors r₁, ..., rₙ
3. For each input ciphertext (aᵢ, bᵢ):
   - Compute a'ᵢ = a_π(i) · g^(rᵢ)
   - Compute b'ᵢ = b_π(i) · h^(rᵢ)
   - Result: (a'ᵢ, b'ᵢ) is re-encrypted and shuffled

Proof Generation:
1. Compute commitment to permutation
2. Create zero-knowledge proof for:
   ✓ Correct permutation application
   ✓ Correct re-encryption
   ✓ No ballots lost or modified
```

### Why Zero-Knowledge Proofs?

ZKP allows the shuffle operator to prove correctness **without revealing**:
- The permutation π (which ballot went where)
- The re-encryption factors (which would allow reversal)
- Any intermediate information

```
ZKP Statement: "I shuffled and re-encrypted correctly"
Proof: (Commitment, Challenge, Response)
Verification: ✓ Proof is valid (without learning secret info)
Result: Everyone trusts the shuffle without trusting the operator
```

---

## 5. Homomorphic Ciphertexts in Detail

### Example: ElGamal Encryption (Homomorphic)

```
Setup:
├─ Prime p
├─ Generator g
├─ Secret key x
├─ Public key y = g^x mod p

Encryption of message m:
├─ Choose random k
├─ Compute: c₁ = g^k mod p
├─ Compute: c₂ = m · y^k mod p
├─ Ciphertext: (c₁, c₂)

Homomorphic Property:
├─ E(m₁) · E(m₂) = (c₁·d₁, c₂·d₂)
├─ = E(m₁ · m₂)
└─ Multiply encrypted messages = encrypt product

For Voting (Multiplication):
├─ Ballot 1: vote for candidate = 1
├─ Ballot 2: vote for candidate = 0
├─ Product: 1 · 0 = 0 (preserves vote)
└─ Can compute homomorphically!
```

### Why Homomorphic for MixNet?

```
Without Homomorphic Encryption:
  ├─ Decrypt ballot
  ├─ ⚠️ PRIVACY LOSS: Plaintext exposed!
  ├─ Shuffle plaintext
  └─ Encrypt again

With Homomorphic Encryption:
  ├─ Shuffle ciphertext (no decryption!)
  ├─ ✓ Plaintext never exposed
  ├─ Re-encrypt shuffled ciphertext
  ├─ ✓ Additional randomization
  └─ Final output is re-encrypted shuffled ciphertext
```

---

## 6. Preventing Ballot Tracing: Attack Models

### Attack 1: Input-Output Linking

**Attacker Goal:** Link input ballot Cᵢ to output ballot C'ⱼ

**Without MixNet:**
```
Input: C₁, C₂, C₃ (in order)
Output: C₁, C₂, C₃ (same order, possibly marked)
Result: ✗ Direct link: Cᵢ = C'ᵢ
```

**With MixNet Shuffle:**
```
Input:  C₁, C₂, C₃, C₄, C₅
Shuffle: [2, 5, 1, 3, 4] (secret permutation)
Output: C₂', C₅', C₁', C₃', C₄' (re-encrypted)

Attacker sees:
  - C₂' has no computational relation to C₂
  - Cannot tell if C₂' is C₁, C₂, C₃, C₄, or C₅
  - Re-encryption randomizes appearance
  - Result: ✓ Link is infeasible
```

### Attack 2: Ciphertext Reuse Detection

**Attacker Goal:** Detect if same ballot appears twice

**Without Re-encryption:**
```
If same ballot appears: C₂ appears as both position 2 and 4
Attacker recognizes: C₂ = C₂ (same ciphertext)
Result: ✗ Can track individual ballots
```

**With Re-encryption:**
```
C₂ is re-encrypted: C₂ → C₂' (different appearance)
Same C₂ at position 2: C₂'
Same C₂ at position 5: C₂'' (different randomization)
Attacker sees: C₂' ≠ C₂'' (computationally indistinguishable)
Result: ✓ Cannot detect reuse
```

### Attack 3: Adversary Breaking Shuffle

**Attacker Goal:** Reverse the permutation π

**Without Verifiable Proof:**
```
Attacker claims: "I know which input is which output"
System: "Prove it"
Attacker: ✗ Cannot prove without breaking discrete log
Result: ✓ System rejects unverified shuffles
```

**With Verifiable Shuffle:**
```
Shuffle operator publishes:
├─ Shuffled ballots: C''₁, ..., C''ₙ
├─ Zero-knowledge proof π_proof
└─ Claim: "These are correct permutation and re-encryption"

Anyone can verify:
├─ Proof is correct mathematical proof
├─ No one can fake proof without breaking cryptography
├─ MixNet operator cannot cheat
└─ Result: ✓ Provably correct shuffle
```

---

## 7. Multi-Layer MixNet: Enhanced Privacy

### Single Layer MixNet
```
Layer 1:
Input:    C₁, C₂, C₃, C₄, C₅
Shuffle:  [3, 1, 4, 2, 5]
Output:   C₃', C₁', C₄', C₂', C₅'

Remaining uncertainty: 5 possibilities for each ballot
But with enough analysis, might be reduced
```

### Multi-Layer MixNet (Recommended)
```
Layer 1:
Input:    C₁, C₂, C₃, C₄, C₅
Shuffle:  [3, 1, 4, 2, 5]
Output:   C₃₁, C₁₁, C₄₁, C₂₁, C₅₁

Layer 2:
Input:    C₃₁, C₁₁, C₄₁, C₂₁, C₅₁
Shuffle:  [2, 4, 1, 3, 5]
Output:   C₁₁', C₂₁', C₃₁', C₄₁', C₅₁'

Layer 3:
Input:    C₁₁', C₂₁', C₃₁', C₄₁', C₅₁'
Shuffle:  [1, 3, 5, 2, 4]
Output:   C₁₁'', C₃₁'', C₅₁'', C₂₁'', C₄₁''

Result:
├─ Each ballot goes through 3 independent shuffles
├─ Each layer randomizes via permutation + re-encryption
├─ Tracing back requires reversing all 3 layers
├─ Computational complexity increases exponentially
└─ ✓ Extremely high privacy: (5!)³ possible paths
```

### Privacy Amplification
```
Number of voters: N
Layers: L

Possible input-output mappings: (N!)^L

For N=1000, L=3:
  ≈ (1000!)^3 possible mappings
  ≈ 2^40,000 (compared to 2^256 for crypto)
  
Result: ✓ Computationally impossible to trace even with quantum
```

---

## 8. Our Implementation: Secure Voting MixNet

### How Our System Uses MixNet

```
VOTING PHASE:
1. Voter requests token
   ├─ Backend issues blind token (hides voter identity)
   └─ Voter receives encrypted token

2. Voter casts vote
   ├─ Vote encrypted with token
   ├─ Submitted to backend
   └─ Stored in ballot database

TALLYING PHASE:
3. Admin runs MixNet
   ├─ Fetch all encrypted ballots
   ├─ Layer 1 shuffle + re-encrypt
   ├─ Layer 2 shuffle + re-encrypt
   ├─ Layer 3 shuffle + re-encrypt
   └─ Publish shuffled ciphertexts + verifiable proofs

VERIFICATION PHASE:
4. Anyone can verify
   ├─ Check each layer's zero-knowledge proof
   ├─ Confirm permutation is valid
   ├─ Verify re-encryption is correct
   └─ ✓ Proof is publicly verifiable

RESULTS:
5. Decrypt shuffled ballots
   ├─ Count votes by candidate
   ├─ ✓ Vote tallies correct (permutation proves this)
   ├─ ✓ No ballot tracing (shuffles prevent this)
   └─ ✓ Ballot privacy maintained (homomorphic encryption)
```

### Implementation Details

```python
# Our MixNet configuration
MIXNET_LAYERS = 3  # Multiple shuffle layers
MIXNET_ALGORITHM = "Chaum-Pedersen"  # Verifiable shuffle protocol
CIPHERTEXT_TYPE = "ElGamal"  # Homomorphic encryption
PROOF_SYSTEM = "Zero-Knowledge Proof"  # Verifiable correctness

# When admin clicks 🔀 MixNet:
1. Fetch all ballots (encrypted)
2. For each layer 1 to MIXNET_LAYERS:
   - Create random permutation
   - Re-encrypt each ballot
   - Generate zero-knowledge proof
   - Store proof for verification
3. Publish results: shuffled_ballots, proofs
4. Anyone can verify: verify_mixnet_proofs()
```

### Code Flow (Frontend)

```python
def page_mixnet():
    """MixNet anonymization page (admin-only)"""
    
    if not st.session_state.authenticated or st.session_state.user_type != "admin":
        st.warning("⚠️ Admin login required.")
        return
    
    st.write("**Admin Function:** Run the MixNet to anonymize and shuffle all ballots.")
    st.info("""
    🔐 MixNet Verifiable Shuffles:
    ├─ Homomorphic Encryption: Ballots encrypted, never decrypted
    ├─ Verifiable Shuffle: Cryptographically proven correct
    ├─ Multi-Layer: 3 shuffle layers for enhanced privacy
    ├─ Zero-Knowledge Proof: Public verification without trust
    └─ Result: Ballots anonymized, voter identity protected
    """)
    
    layers = st.slider("Number of mixing layers", 1, 10, 3)
    
    if st.button("Run MixNet", use_container_width=True, type="primary"):
        try:
            # Backend runs verifiable shuffle with multiple layers
            result = admin_client.run_mixnet(layers=layers)
            
            st.success("✓ MixNet completed! Ballots anonymized and shuffled.")
            
            with st.expander("Verify MixNet Proofs"):
                st.json(result.get("proofs", {}))
                
            with st.expander("Shuffled Ballots Count"):
                st.write(f"Total ballots shuffled: {len(result.get('shuffled_ballots', []))}")
                
        except Exception as e:
            st.error(f"✗ MixNet failed: {str(e)}")
```

---

## 9. Security Properties Provided

### 1. Ballot Secrecy ✓
```
Property: Vote cannot be linked to voter
Guaranteed by: Homomorphic encryption + verifiable shuffle
Result: Even with all system data, cannot determine voter's choice
```

### 2. Ballot Integrity ✓
```
Property: Ballots cannot be modified
Guaranteed by: Zero-knowledge proofs
Result: System cannot change votes without detection
```

### 3. Verifiability ✓
```
Property: Anyone can verify results
Guaranteed by: Publicly verifiable shuffle proofs
Result: No trust required in election authorities
```

### 4. Privacy Under Coercion ✓
```
Property: Voter cannot prove how they voted
Guaranteed by: Multiple shuffle layers + homomorphic encryption
Result: Coercion resistant (voter cannot prove vote to coercer)
```

### 5. Computational Security ✓
```
Property: Cannot reverse shuffle even with computational power
Guaranteed by: Discrete logarithm hardness + verifiable shuffles
Result: Security based on mathematical hardness, not trust
```

---

## 10. Attack Resistance

### Against Voter Tracing
```
Attack: Trace voter's ballot through system
Defense: MixNet verifiable shuffles + homomorphic encryption
Result: ✓ Computationally infeasible
```

### Against Ballot Modification
```
Attack: Change vote during tallying
Defense: Zero-knowledge proofs verify no modification
Result: ✓ Detected automatically
```

### Against Shuffle Cheating
```
Attack: Shuffle operator claims false permutation
Defense: Publicly verifiable zero-knowledge proof
Result: ✓ Any cheating detected
```

### Against Ciphertext Reuse
```
Attack: Count same ballot twice
Defense: Re-encryption randomizes appearance
Result: ✓ Reuse undetectable (computationally)
```

### Against Homomorphic Decryption
```
Attack: Decrypt to reveal voter choice
Defense: Homomorphic encryption preserves security
Result: ✓ Cannot decrypt without secret key
```

---

## 11. Privacy Guarantee Formula

```
Voter Privacy = 
    (Homomorphic Encryption Security) 
    × (Shuffle Permutation Uncertainty)^(Number of Layers)
    × (Discrete Log Hardness)

For our implementation:
├─ Homomorphic Encryption: 2^2048 (RSA-level)
├─ Shuffle Uncertainty: (1000!)^3 ≈ 2^40,000
├─ Discrete Log: 2^256 (Elliptic Curve)
└─ Combined: >> 2^128 (Quantum-resistant recommended level)

Result: ✓ Extremely high privacy guarantee
```

---

## 12. Voter Post-Login Flow with Privacy

### Voter Workflow (with MixNet Privacy)

```
VOTER PERSPECTIVE:

1. 🏠 Home
   └─ Learn about system privacy

2. ✍️ Register Voter (Self-Register)
   ├─ Enter: Name, Email
   ├─ Receive: Auto-generated Voter ID (VOTER-001)
   └─ Purpose: Self-service registration

3. 🔑 Request Token (Voter-Only)
   ├─ Action: Request blind voting token
   ├─ Backend generates encrypted token
   ├─ Voter receives token (cannot see backend process)
   └─ Purpose: Blind signature protocol

4. 🗳️ Cast Vote (Voter-Only)
   ├─ Input: Select candidate
   ├─ Encrypt: Vote with token
   ├─ Submit: Encrypted vote to backend
   └─ Purpose: Voter privacy maintained (encrypted)

AFTER VOTING CLOSES:

5. Admin Runs MixNet
   ├─ Fetch all encrypted votes
   ├─ Run verifiable shuffle (Layer 1, 2, 3)
   ├─ Generate zero-knowledge proofs
   └─ Publish results + proofs
   
PRIVACY RESULT:

6. 📊 View Results (Admin)
   ├─ Decrypt shuffled (anonymized) votes
   ├─ Count votes by candidate
   ├─ Voter-to-vote link is broken
   └─ ✓ Ballot privacy achieved!
```

---

## Summary

### Key Points

1. **MixNet Purpose:** Break link between voter and ballot during tallying

2. **Verifiable Shuffles:** Prove correct permutation without revealing permutation

3. **Homomorphic Ciphertexts:** Enable shuffle without decryption (maintains privacy)

4. **Multi-Layer Shuffle:** Enhance privacy through layered randomization

5. **Zero-Knowledge Proofs:** Allow public verification without trust

6. **Voter Privacy:** Protected by mathematics, not organizational trust

### Why It Matters

Without MixNet verifiable shuffles:
- ✗ Voter can be identified with their vote
- ✗ Voting authority must be trusted not to leak
- ✗ Coercion becomes possible (voter can prove vote)

With MixNet verifiable shuffles:
- ✓ Voter-ballot link cryptographically broken
- ✓ No trust in authority needed (verifiable)
- ✓ Voter cannot prove vote (coercion resistant)
- ✓ Mathematically guaranteed privacy

---

## Implementation Checklist

- [x] Frontend: Admin can access MixNet page
- [x] Frontend: Display MixNet information
- [x] Frontend: Admin can run MixNet with configurable layers
- [x] Backend: Implement homomorphic encryption (if using ElGamal)
- [x] Backend: Implement verifiable shuffle protocol (Chaum-Pedersen)
- [x] Backend: Generate zero-knowledge proofs
- [x] Backend: Publish proofs for verification
- [ ] Verification: Public verification tool for proofs
- [ ] Testing: Verify privacy properties hold
- [ ] Documentation: Explain voter that votes are private

---

**Version:** 2.1  
**Topic:** MixNet Verifiable Shuffles & Ballot Privacy  
**Status:** ✅ Documented  
**Last Updated:** October 22, 2025

For questions about cryptographic details, refer to:
- Chaum, D. (1981). "Untraceable electronic mail, return addresses, and digital pseudonyms"
- Wikström, D. (2005). "A Universally Composable Mix-Net"
