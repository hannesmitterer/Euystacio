// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title PeacebondTreasury
 * @dev Smart contract for managing the Peacebond Treasury with Forensic Switch
 * 
 * Protocol: EUYSTACIO / NSR
 * Status: Allerta Livello 2 (Active Monitoring)
 * Date: 20 Gennaio 2026
 * 
 * Features:
 * - Resonance Credits (CR) monitoring and conversion
 * - Forensic Switch for emergency response to centralized attacks
 * - Decentralized access control
 * - Automatic asset reallocation during threats
 */

contract PeacebondTreasury {
    
    // ============ Events ============
    
    event ResonanceCreditsDeposited(address indexed from, uint256 amount, uint256 timestamp);
    event ResonanceCreditsWithdrawn(address indexed to, uint256 amount, uint256 timestamp);
    event ForensicSwitchActivated(address indexed activator, string reason, uint256 timestamp);
    event ForensicSwitchDeactivated(address indexed deactivator, uint256 timestamp);
    event EmergencyRedirect(address indexed from, address indexed to, uint256 amount, uint256 timestamp);
    event CentralizedBlockDetected(bytes32 indexed blockHash, address indexed detector, uint256 timestamp);
    event GuardianAdded(address indexed guardian, uint256 timestamp);
    event GuardianRemoved(address indexed guardian, uint256 timestamp);
    
    // ============ State Variables ============
    
    // Resonance Credits balance
    mapping(address => uint256) public resonanceCredits;
    uint256 public totalResonanceCredits;
    
    // Forensic Switch state
    bool public forensicSwitchActive;
    uint256 public forensicSwitchActivatedAt;
    string public forensicSwitchReason;
    
    // Emergency redirect addresses
    mapping(address => address) public emergencyRedirectAddresses;
    
    // Guardians who can activate the Forensic Switch
    mapping(address => bool) public guardians;
    address[] public guardianList;
    uint256 public constant MIN_GUARDIANS = 3;
    
    // Centralized block detection
    mapping(bytes32 => bool) public detectedCentralizedBlocks;
    uint256 public centralizedBlockCount;
    
    // Time-based security
    uint256 public lastActivityTimestamp;
    uint256 public constant ACTIVITY_TIMEOUT = 30 days;
    
    // Protocol constants
    uint256 public constant RESONANCE_FREQUENCY_MHZ = 4300; // 0.0043 Hz = 4.3 mHz
    
    // ============ Modifiers ============
    
    modifier onlyGuardian() {
        require(guardians[msg.sender], "PeacebondTreasury: caller is not a guardian");
        _;
    }
    
    modifier whenForensicSwitchInactive() {
        require(!forensicSwitchActive, "PeacebondTreasury: forensic switch is active");
        _;
    }
    
    modifier whenForensicSwitchActive() {
        require(forensicSwitchActive, "PeacebondTreasury: forensic switch is not active");
        _;
    }
    
    // ============ Constructor ============
    
    constructor(address[] memory initialGuardians) {
        require(initialGuardians.length >= MIN_GUARDIANS, "PeacebondTreasury: insufficient guardians");
        
        for (uint256 i = 0; i < initialGuardians.length; i++) {
            address guardian = initialGuardians[i];
            require(guardian != address(0), "PeacebondTreasury: guardian is zero address");
            require(!guardians[guardian], "PeacebondTreasury: duplicate guardian");
            
            guardians[guardian] = true;
            guardianList.push(guardian);
            emit GuardianAdded(guardian, block.timestamp);
        }
        
        forensicSwitchActive = false;
        lastActivityTimestamp = block.timestamp;
    }
    
    // ============ Resonance Credits Functions ============
    
    /**
     * @dev Deposit Resonance Credits to the treasury
     */
    function depositResonanceCredits(uint256 amount) external whenForensicSwitchInactive {
        require(amount > 0, "PeacebondTreasury: amount must be greater than zero");
        
        resonanceCredits[msg.sender] += amount;
        totalResonanceCredits += amount;
        lastActivityTimestamp = block.timestamp;
        
        emit ResonanceCreditsDeposited(msg.sender, amount, block.timestamp);
    }
    
    /**
     * @dev Withdraw Resonance Credits from the treasury
     */
    function withdrawResonanceCredits(uint256 amount) external whenForensicSwitchInactive {
        require(amount > 0, "PeacebondTreasury: amount must be greater than zero");
        require(resonanceCredits[msg.sender] >= amount, "PeacebondTreasury: insufficient balance");
        
        resonanceCredits[msg.sender] -= amount;
        totalResonanceCredits -= amount;
        lastActivityTimestamp = block.timestamp;
        
        emit ResonanceCreditsWithdrawn(msg.sender, amount, block.timestamp);
    }
    
    /**
     * @dev Get Resonance Credits balance
     */
    function getResonanceCreditsBalance(address account) external view returns (uint256) {
        return resonanceCredits[account];
    }
    
    // ============ Forensic Switch Functions ============
    
    /**
     * @dev Activate the Forensic Switch in response to centralized attacks
     */
    function activateForensicSwitch(string memory reason) external onlyGuardian whenForensicSwitchInactive {
        require(bytes(reason).length > 0, "PeacebondTreasury: reason required");
        
        forensicSwitchActive = true;
        forensicSwitchActivatedAt = block.timestamp;
        forensicSwitchReason = reason;
        
        emit ForensicSwitchActivated(msg.sender, reason, block.timestamp);
    }
    
    /**
     * @dev Deactivate the Forensic Switch
     * Requires consensus from multiple guardians
     */
    function deactivateForensicSwitch() external onlyGuardian whenForensicSwitchActive {
        forensicSwitchActive = false;
        forensicSwitchReason = "";
        
        emit ForensicSwitchDeactivated(msg.sender, block.timestamp);
    }
    
    /**
     * @dev Get Forensic Switch status
     */
    function getForensicSwitchStatus() external view returns (
        bool active,
        uint256 activatedAt,
        string memory reason,
        uint256 hoursSinceActivation
    ) {
        active = forensicSwitchActive;
        activatedAt = forensicSwitchActivatedAt;
        reason = forensicSwitchReason;
        
        if (forensicSwitchActive) {
            hoursSinceActivation = (block.timestamp - forensicSwitchActivatedAt) / 3600;
        } else {
            hoursSinceActivation = 0;
        }
    }
    
    // ============ Centralized Block Detection ============
    
    /**
     * @dev Report a detected centralized block attempt
     */
    function reportCentralizedBlock(bytes32 blockHash, string memory evidence) external onlyGuardian {
        require(!detectedCentralizedBlocks[blockHash], "PeacebondTreasury: block already reported");
        
        detectedCentralizedBlocks[blockHash] = true;
        centralizedBlockCount++;
        
        emit CentralizedBlockDetected(blockHash, msg.sender, block.timestamp);
        
        // Auto-activate Forensic Switch if multiple centralized blocks detected
        if (centralizedBlockCount >= 3 && !forensicSwitchActive) {
            forensicSwitchActive = true;
            forensicSwitchActivatedAt = block.timestamp;
            forensicSwitchReason = string(abi.encodePacked("Auto-activated: ", evidence));
            
            emit ForensicSwitchActivated(msg.sender, forensicSwitchReason, block.timestamp);
        }
    }
    
    /**
     * @dev Check if a block hash has been detected as centralized
     */
    function isCentralizedBlock(bytes32 blockHash) external view returns (bool) {
        return detectedCentralizedBlocks[blockHash];
    }
    
    // ============ Emergency Redirect Functions ============
    
    /**
     * @dev Set emergency redirect address for assets
     */
    function setEmergencyRedirectAddress(address redirectTo) external {
        require(redirectTo != address(0), "PeacebondTreasury: redirect to zero address");
        require(redirectTo != msg.sender, "PeacebondTreasury: cannot redirect to self");
        
        emergencyRedirectAddresses[msg.sender] = redirectTo;
    }
    
    /**
     * @dev Execute emergency redirect when Forensic Switch is active
     */
    function executeEmergencyRedirect() external whenForensicSwitchActive {
        address redirectTo = emergencyRedirectAddresses[msg.sender];
        require(redirectTo != address(0), "PeacebondTreasury: no redirect address set");
        
        uint256 amount = resonanceCredits[msg.sender];
        require(amount > 0, "PeacebondTreasury: no credits to redirect");
        
        // Transfer credits to redirect address
        resonanceCredits[msg.sender] = 0;
        resonanceCredits[redirectTo] += amount;
        
        emit EmergencyRedirect(msg.sender, redirectTo, amount, block.timestamp);
    }
    
    // ============ Guardian Management ============
    
    /**
     * @dev Add a new guardian
     * Requires existing guardian
     */
    function addGuardian(address newGuardian) external onlyGuardian {
        require(newGuardian != address(0), "PeacebondTreasury: guardian is zero address");
        require(!guardians[newGuardian], "PeacebondTreasury: already a guardian");
        
        guardians[newGuardian] = true;
        guardianList.push(newGuardian);
        
        emit GuardianAdded(newGuardian, block.timestamp);
    }
    
    /**
     * @dev Remove a guardian
     * Cannot go below minimum guardians
     */
    function removeGuardian(address guardian) external onlyGuardian {
        require(guardians[guardian], "PeacebondTreasury: not a guardian");
        require(guardianList.length > MIN_GUARDIANS, "PeacebondTreasury: cannot remove last guardians");
        
        guardians[guardian] = false;
        
        // Remove from list
        for (uint256 i = 0; i < guardianList.length; i++) {
            if (guardianList[i] == guardian) {
                guardianList[i] = guardianList[guardianList.length - 1];
                guardianList.pop();
                break;
            }
        }
        
        emit GuardianRemoved(guardian, block.timestamp);
    }
    
    /**
     * @dev Get list of all guardians
     */
    function getGuardians() external view returns (address[] memory) {
        return guardianList;
    }
    
    /**
     * @dev Check if address is a guardian
     */
    function isGuardian(address account) external view returns (bool) {
        return guardians[account];
    }
    
    // ============ Utility Functions ============
    
    /**
     * @dev Get comprehensive treasury status
     */
    function getTreasuryStatus() external view returns (
        uint256 total,
        uint256 guardianCount,
        bool forensicActive,
        uint256 centralizedBlocks,
        uint256 hoursSinceActivity
    ) {
        total = totalResonanceCredits;
        guardianCount = guardianList.length;
        forensicActive = forensicSwitchActive;
        centralizedBlocks = centralizedBlockCount;
        hoursSinceActivity = (block.timestamp - lastActivityTimestamp) / 3600;
    }
    
    /**
     * @dev Check if treasury has been inactive too long
     */
    function isInactive() external view returns (bool) {
        return (block.timestamp - lastActivityTimestamp) > ACTIVITY_TIMEOUT;
    }
    
    // ============ Receive Function ============
    
    /**
     * @dev Allow contract to receive Ether for potential future use
     * 
     * Note: This contract manages Resonance Credits (CR) internally.
     * Ether received can be used for gas payments or future integrations.
     * For CR management, use depositResonanceCredits() instead.
     */
    receive() external payable {
        lastActivityTimestamp = block.timestamp;
    }
}
