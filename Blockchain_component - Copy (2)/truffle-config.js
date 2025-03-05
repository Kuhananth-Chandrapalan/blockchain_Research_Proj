const HDWalletProvider = require('@truffle/hdwallet-provider');
require('dotenv').config(); // To load MNEMONIC and INFURA_PROJECT_ID from a .env file

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 7545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
    },
  },

  compilers: {
    solc: {
      version: "0.5.16",      // Use Solidity version 0.5.16
    }
  }
};
