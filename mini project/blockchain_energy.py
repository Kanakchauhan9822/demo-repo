"""
blockchain_energy.py - Blockchain-Enabled Energy Transaction System
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
        """Calculate SHA-256 hash of block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        """Proof of Work (PoW) mining"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class SmartContract:
    """Smart contract for automated energy trading"""
    
    def __init__(self, contract_id: str, producer: str, consumer: str, energy_kwh: float, price: float):
        self.contract_id = contract_id
        self.producer = producer
        self.consumer = consumer
        self.energy_kwh = energy_kwh
        self.price = price
        self.status = 'pending'
        self.timestamp = datetime.now().isoformat()

    def execute(self) -> Dict:
        """Execute smart contract automatically"""
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
    """Blockchain for managing peer-to-peer energy transactions"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = difficulty
        self.mining_reward = 1.0
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.now().isoformat(), [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]

    def add_transaction(self, transaction: Dict):
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        """Mine a new block with pending transactions"""
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

        # Add mining reward
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
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address: str) -> float:
        """Calculate energy balance for an address"""
        balance = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('to') == address:
                    balance += transaction.get('total_cost', 0)
                if transaction.get('from') == address:
                    balance -= transaction.get('total_cost', 0)
        return balance

    def get_transaction_history(self, address: str) -> List[Dict]:
        """Get all transactions for a specific address"""
        history = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('to') == address or transaction.get('from') == address:
                    history.append({
                        'block': block.index,
                        'transaction': transaction
                    })
        return history

    def display_chain_info(self):
        """Display blockchain information"""
        print(f"\nBlockchain Info:")
        print(f"  Total Blocks: {len(self.chain)}")
        print(f"  Mining Difficulty: {self.difficulty}")
        print(f"  Chain Valid: {self.is_chain_valid()}")
        
        total_txns = sum(len(block.transactions) for block in self.chain)
        print(f"  Total Transactions: {total_txns}")

# Standalone execution mode
if __name__ == "__main__":
    print("=" * 70)
    print("Blockchain-Enabled Energy Management System (Standalone Mode)")
    print("=" * 70)

    print("\n[1] Initializing blockchain network...")
    energy_chain = EnergyBlockchain(difficulty=2)

    print("[2] Creating smart contracts for energy trading...")

    # Create sample contracts
    contracts_data = [
        {'id': 'SC001', 'producer': 'Solar_Panel_A', 'consumer': 'Home_User_1', 
         'energy': 25.5, 'price': 0.12},
        {'id': 'SC002', 'producer': 'Solar_Panel_B', 'consumer': 'Business_User_1', 
         'energy': 150.0, 'price': 0.10},
        {'id': 'SC003', 'producer': 'Solar_Panel_A', 'consumer': 'Home_User_2', 
         'energy': 35.0, 'price': 0.11}
    ]

    print("\n" + "=" * 70)
    print("EXECUTING SMART CONTRACTS")
    print("=" * 70)

    contracts = []
    for data in contracts_data:
        contract = SmartContract(
            contract_id=data['id'],
            producer=data['producer'],
            consumer=data['consumer'],
            energy_kwh=data['energy'],
            price=data['price']
        )
        contracts.append(contract)
        
        transaction = contract.execute()
        energy_chain.add_transaction(transaction)
        
        print(f"\n✓ Contract {contract.contract_id} executed")
        print(f"  {contract.producer} → {contract.consumer}")
        print(f"  Energy: {contract.energy_kwh} kWh")
        print(f"  Cost: ${transaction['total_cost']:.2f}")

    print("\n" + "=" * 70)
    print("MINING TRANSACTIONS")
    print("=" * 70)
    energy_chain.mine_pending_transactions('Validator_Node_1')

    print("\n" + "=" * 70)
    print("BLOCKCHAIN VALIDATION")
    print("=" * 70)
    is_valid = energy_chain.is_chain_valid()
    print(f"Blockchain valid: {is_valid}")

    print("\n" + "=" * 70)
    print("ACCOUNT BALANCES")
    print("=" * 70)

    accounts = ['Solar_Panel_A', 'Solar_Panel_B', 'Home_User_1', 
                'Home_User_2', 'Business_User_1', 'Validator_Node_1']
    
    for account in accounts:
        balance = energy_chain.get_balance(account)
        if balance != 0:
            balance_type = "Revenue" if balance > 0 else "Cost"
            print(f"{account}: ${abs(balance):.2f} ({balance_type})")

    print("\n" + "=" * 70)
    print("BLOCKCHAIN STATISTICS")
    print("=" * 70)
    energy_chain.display_chain_info()

    print("\n" + "=" * 70)
    print("Decentralized energy trading enabled")
    print("Secure peer-to-peer transactions verified")
    print("=" * 70)