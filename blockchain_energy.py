"""
Blockchain-Enabled Energy Transaction System
Implements decentralized energy trading using blockchain
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict

class Block:
    """
    Represents a single block in the blockchain
    Contains energy transaction data
    """
    def __init__(self, index: int, timestamp: str, transactions: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate SHA-256 hash of block
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        """
        Proof of Work (PoW) mining
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class SmartContract:
    """
    Smart contract for automated energy trading
    """
    def __init__(self, contract_id: str, producer: str, consumer: str, energy_kwh: float, price: float):
        self.contract_id = contract_id
        self.producer = producer
        self.consumer = consumer
        self.energy_kwh = energy_kwh
        self.price = price
        self.status = 'pending'
        self.timestamp = datetime.now().isoformat()

    def execute(self) -> Dict:
        """
        Execute smart contract automatically
        """
        transaction = {
            'contract_id': self.contract_id,
            'from': self.producer,
            'to': self.consumer,
            'energy_kwh': self.energy_kwh,
            'price_per_kwh': self.price,
            'total_cost': self.energy_kwh * self.price,
            'timestamp': self.timestamp,
            'type': 'energy_trade'
        }
        self.status = 'completed'
        return transaction

class EnergyBlockchain:
    """
    Blockchain for managing peer-to-peer energy transactions
    """
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = difficulty
        self.mining_reward = 1.0
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the chain
        """
        genesis_block = Block(0, datetime.now().isoformat(), [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """
        Get the most recent block
        """
        return self.chain[-1]

    def add_transaction(self, transaction: Dict):
        """
        Add transaction to pending pool
        """
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        """
        Mine a new block with pending transactions
        """
        if not self.pending_transactions:
            print("No transactions to mine")
            return

        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        print(f"Mining block {new_block.index}...")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        reward_transaction = {
            'from': 'network',
            'to': miner_address,
            'energy_kwh': 0,
            'price_per_kwh': 0,
            'total_cost': self.mining_reward,
            'type': 'mining_reward'
        }
        self.pending_transactions = [reward_transaction]

        print(f"Block {new_block.index} mined successfully!")

    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address: str) -> float:
        """
        Calculate energy balance for an address
        """
        balance = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('to') == address:
                    balance += transaction.get('total_cost', 0)
                if transaction.get('from') == address:
                    balance -= transaction.get('total_cost', 0)
        return balance

def main():
    print("=" * 70)
    print("Blockchain-Enabled Energy Management System")
    print("=" * 70)

    print("\n[1] Initializing blockchain network...")
    energy_chain = EnergyBlockchain(difficulty=2)

    print("[2] Creating smart contracts for energy trading...")

    contract1 = SmartContract(
        contract_id='SC001',
        producer='Solar_Panel_A',
        consumer='Home_User_1',
        energy_kwh=25.5,
        price=0.12
    )

    contract2 = SmartContract(
        contract_id='SC002',
        producer='Solar_Panel_B',
        consumer='Business_User_1',
        energy_kwh=150.0,
        price=0.10
    )

    contract3 = SmartContract(
        contract_id='SC003',
        producer='Solar_Panel_A',
        consumer='Home_User_2',
        energy_kwh=35.0,
        price=0.11
    )

    print("\n" + "=" * 70)
    print("EXECUTING SMART CONTRACTS")
    print("=" * 70)

    transaction1 = contract1.execute()
    energy_chain.add_transaction(transaction1)
    print(f"\n✓ Contract {contract1.contract_id} executed")
    print(f"  {contract1.producer} → {contract1.consumer}")
    print(f"  Energy: {contract1.energy_kwh} kWh")
    print(f"  Cost: ${transaction1['total_cost']:.2f}")

    transaction2 = contract2.execute()
    energy_chain.add_transaction(transaction2)
    print(f"\n✓ Contract {contract2.contract_id} executed")
    print(f"  {contract2.producer} → {contract2.consumer}")
    print(f"  Energy: {contract2.energy_kwh} kWh")
    print(f"  Cost: ${transaction2['total_cost']:.2f}")

    print("\n" + "=" * 70)
    print("MINING TRANSACTIONS")
    print("=" * 70)
    energy_chain.mine_pending_transactions('Validator_Node_1')

    transaction3 = contract3.execute()
    energy_chain.add_transaction(transaction3)
    print(f"\n✓ Contract {contract3.contract_id} executed")
    print(f"  {contract3.producer} → {contract3.consumer}")
    print(f"  Energy: {contract3.energy_kwh} kWh")
    print(f"  Cost: ${transaction3['total_cost']:.2f}")

    print("\n" + "=" * 70)
    energy_chain.mine_pending_transactions('Validator_Node_2')

    print("\n" + "=" * 70)
    print("BLOCKCHAIN VALIDATION")
    print("=" * 70)
    is_valid = energy_chain.is_chain_valid()
    print(f"Blockchain valid: {is_valid}")

    print("\n" + "=" * 70)
    print("ACCOUNT BALANCES")
    print("=" * 70)

    accounts = ['Solar_Panel_A', 'Solar_Panel_B', 'Home_User_1', 'Home_User_2', 'Business_User_1']
    for account in accounts:
        balance = energy_chain.get_balance(account)
        balance_type = "Revenue" if balance > 0 else "Cost"
        print(f"{account}: ${abs(balance):.2f} ({balance_type})")

    print("\n" + "=" * 70)
    print("BLOCKCHAIN STATISTICS")
    print("=" * 70)
    print(f"Total Blocks: {len(energy_chain.chain)}")
    print(f"Total Transactions: {sum(len(block.transactions) for block in energy_chain.chain)}")
    print(f"Mining Difficulty: {energy_chain.difficulty}")
    print(f"Chain Integrity: {'Verified ✓' if is_valid else 'Compromised ✗'}")

    print("\n" + "=" * 70)
    print("Decentralized energy trading enabled")
    print("Secure peer-to-peer transactions verified")
    print("=" * 70)

if __name__ == "__main__":
    main()
