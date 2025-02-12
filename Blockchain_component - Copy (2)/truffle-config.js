const HDWalletProvider = require('@truffle/hdwallet-provider');
require('dotenv').config(); // To load MNEMONIC and INFURA_PROJECT_ID from a .env file

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 7545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
    },
    sepolia: {
      provider: () => new HDWalletProvider(
        process.env.MNEMONIC, // Your 12-word mnemonic from MetaMask
        `https://sepolia.infura.io/v3/${process.env.INFURA_PROJECT_ID}` // Infura endpoint
      ),
      network_id: 11155111,   // Sepolia's network ID
      gas: 3000000,           // Gas limit
      gasPrice: 20000000000,  // 20 gwei (in wei)
      confirmations: 2,       // Wait for 2 confirmations
      timeoutBlocks: 200,     // Wait for 200 blocks before timing out
      skipDryRun: true        // Skip dry run before migrations
    },
  },

  mocha: {
    // timeout: 100000
  },

  compilers: {
    solc: {
      version: "0.5.16",      // Use Solidity version 0.5.16
    }
  }
};
