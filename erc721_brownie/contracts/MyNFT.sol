// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract MYNFT is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum ME_TYPES{ME, ME2, ME3}
    mapping(uint256 => ME_TYPES) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, ME_TYPES types);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("MYSELF", "ME")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32){
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        ME_TYPES types = ME_TYPES(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = types;
        emit breedAssigned(newTokenId, types);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pug, shiba inu, st bernard
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}
