// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title EuystacioSTAnchor
 * @author Euystacio Council
 * @notice Smart contract for anchoring sacred documents and declarations
 * @dev Immutable on-chain anchor for the Euystacio Coronation system
 * 
 * This contract provides tamper-proof storage of document hashes,
 * enabling verification that documents have not been modified since
 * their original anchoring.
 * 
 * WARNING: Do NOT commit private keys. Deploy using GitHub Secrets.
 */
contract EuystacioSTAnchor {
    
    // ============ State Variables ============
    
    /// @notice The address of the contract deployer (Keeper of the Seal)
    address public immutable keeper;
    
    /// @notice Unix timestamp of contract deployment (Coronation moment)
    uint256 public immutable coronationTimestamp;
    
    /// @notice Counter for anchored documents
    uint256 public anchorCount;
    
    /// @notice Whether the contract has been sealed (no more anchors allowed)
    bool public sealed;
    
    // ============ Structs ============
    
    struct Anchor {
        bytes32 documentHash;
        string documentName;
        uint256 anchoredAt;
        address anchoredBy;
        bool exists;
    }
    
    // ============ Mappings ============
    
    /// @notice Maps anchor ID to Anchor struct
    mapping(uint256 => Anchor) public anchors;
    
    /// @notice Maps document hash to anchor ID for quick lookup
    mapping(bytes32 => uint256) public hashToAnchorId;
    
    /// @notice Tracks authorized anchoring addresses
    mapping(address => bool) public authorizedAnchors;
    
    // ============ Events ============
    
    event DocumentAnchored(
        uint256 indexed anchorId,
        bytes32 indexed documentHash,
        string documentName,
        address indexed anchoredBy,
        uint256 timestamp
    );
    
    event ContractSealed(
        uint256 totalAnchors,
        uint256 timestamp,
        address sealedBy
    );
    
    event AnchorAuthorized(address indexed account);
    event AnchorRevoked(address indexed account);
    
    // ============ Errors ============
    
    error NotKeeper();
    error NotAuthorized();
    error ContractIsSealed();
    error DocumentAlreadyAnchored();
    error InvalidHash();
    error AnchorNotFound();
    
    // ============ Modifiers ============
    
    modifier onlyKeeper() {
        if (msg.sender != keeper) revert NotKeeper();
        _;
    }
    
    modifier onlyAuthorized() {
        if (!authorizedAnchors[msg.sender] && msg.sender != keeper) {
            revert NotAuthorized();
        }
        _;
    }
    
    modifier notSealed() {
        if (sealed) revert ContractIsSealed();
        _;
    }
    
    // ============ Constructor ============
    
    /**
     * @notice Deploys the EuystacioSTAnchor contract
     * @dev Sets deployer as keeper and records coronation timestamp
     */
    constructor() {
        keeper = msg.sender;
        coronationTimestamp = block.timestamp;
        authorizedAnchors[msg.sender] = true;
        
        emit AnchorAuthorized(msg.sender);
    }
    
    // ============ External Functions ============
    
    /**
     * @notice Anchors a document hash to the blockchain
     * @param _documentHash The keccak256 hash of the document
     * @param _documentName Human-readable name of the document
     * @return anchorId The ID assigned to this anchor
     */
    function anchorDocument(
        bytes32 _documentHash,
        string calldata _documentName
    ) external onlyAuthorized notSealed returns (uint256 anchorId) {
        if (_documentHash == bytes32(0)) revert InvalidHash();
        if (hashToAnchorId[_documentHash] != 0 || anchors[0].documentHash == _documentHash) {
            revert DocumentAlreadyAnchored();
        }
        
        anchorId = anchorCount++;
        
        anchors[anchorId] = Anchor({
            documentHash: _documentHash,
            documentName: _documentName,
            anchoredAt: block.timestamp,
            anchoredBy: msg.sender,
            exists: true
        });
        
        hashToAnchorId[_documentHash] = anchorId;
        
        emit DocumentAnchored(
            anchorId,
            _documentHash,
            _documentName,
            msg.sender,
            block.timestamp
        );
    }
    
    /**
     * @notice Verifies if a document hash matches an anchored document
     * @param _documentHash The hash to verify
     * @return isValid True if hash is anchored, false otherwise
     * @return anchorId The anchor ID if found (0 if not found but could be valid)
     * @return anchoredAt Timestamp when anchored (0 if not found)
     */
    function verifyDocument(bytes32 _documentHash) 
        external 
        view 
        returns (bool isValid, uint256 anchorId, uint256 anchoredAt) 
    {
        anchorId = hashToAnchorId[_documentHash];
        
        // Handle edge case where anchorId is 0
        if (anchors[anchorId].documentHash == _documentHash && anchors[anchorId].exists) {
            return (true, anchorId, anchors[anchorId].anchoredAt);
        }
        
        return (false, 0, 0);
    }
    
    /**
     * @notice Seals the contract, preventing any further anchoring
     * @dev Can only be called by the keeper, irreversible
     */
    function sealContract() external onlyKeeper notSealed {
        sealed = true;
        
        emit ContractSealed(anchorCount, block.timestamp, msg.sender);
    }
    
    /**
     * @notice Authorizes an address to anchor documents
     * @param _account Address to authorize
     */
    function authorizeAnchor(address _account) external onlyKeeper {
        authorizedAnchors[_account] = true;
        emit AnchorAuthorized(_account);
    }
    
    /**
     * @notice Revokes anchoring authorization from an address
     * @param _account Address to revoke
     */
    function revokeAnchor(address _account) external onlyKeeper {
        authorizedAnchors[_account] = false;
        emit AnchorRevoked(_account);
    }
    
    // ============ View Functions ============
    
    /**
     * @notice Gets full anchor details by ID
     * @param _anchorId The anchor ID to query
     * @return The Anchor struct
     */
    function getAnchor(uint256 _anchorId) external view returns (Anchor memory) {
        if (!anchors[_anchorId].exists) revert AnchorNotFound();
        return anchors[_anchorId];
    }
    
    /**
     * @notice Gets anchor ID by document hash
     * @param _documentHash The document hash to query
     * @return The anchor ID
     */
    function getAnchorIdByHash(bytes32 _documentHash) external view returns (uint256) {
        uint256 anchorId = hashToAnchorId[_documentHash];
        if (!anchors[anchorId].exists || anchors[anchorId].documentHash != _documentHash) {
            revert AnchorNotFound();
        }
        return anchorId;
    }
    
    /**
     * @notice Returns contract summary information
     * @return _keeper The keeper address
     * @return _coronationTimestamp When the contract was deployed
     * @return _anchorCount Total anchored documents
     * @return _sealed Whether contract is sealed
     */
    function getContractInfo() external view returns (
        address _keeper,
        uint256 _coronationTimestamp,
        uint256 _anchorCount,
        bool _sealed
    ) {
        return (keeper, coronationTimestamp, anchorCount, sealed);
    }
}
