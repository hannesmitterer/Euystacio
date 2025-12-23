#!/bin/bash

#########################################
# Euystacio IPFS Eternalization Script
# Automates the complete workflow for eternalizing frameworks using IPFS and Pinata
#########################################

set -e  # Exit on error

# Color codes for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCS_DIR="docs"
IPFS_DIR="$HOME/.ipfs"
IPFS_VERSION="v0.28.0"
IPFS_DIST_URL="https://dist.ipfs.tech/kubo/${IPFS_VERSION}"

#########################################
# Helper Functions
#########################################

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

#########################################
# Step 1: Check and Install IPFS CLI
#########################################

install_ipfs() {
    print_section "Step 1: IPFS CLI Installation"
    
    if command -v ipfs &> /dev/null; then
        local current_version=$(ipfs --version | awk '{print $3}')
        print_success "IPFS CLI already installed (version: $current_version)"
        return 0
    fi
    
    print_info "IPFS CLI not found. Installing IPFS CLI ${IPFS_VERSION}..."
    
    # Detect OS and architecture
    local os=$(uname -s | tr '[:upper:]' '[:lower:]')
    local arch=$(uname -m)
    
    case "$arch" in
        x86_64)
            arch="amd64"
            ;;
        aarch64|arm64)
            arch="arm64"
            ;;
        armv7l)
            arch="arm"
            ;;
        *)
            print_error "Unsupported architecture: $arch"
            exit 1
            ;;
    esac
    
    case "$os" in
        linux|darwin)
            ;;
        *)
            print_error "Unsupported operating system: $os"
            exit 1
            ;;
    esac
    
    local filename="kubo_${IPFS_VERSION}_${os}-${arch}.tar.gz"
    local download_url="${IPFS_DIST_URL}/${filename}"
    
    print_info "Downloading IPFS from: $download_url"
    
    # Create temporary directory
    local tmp_dir=$(mktemp -d)
    cd "$tmp_dir"
    
    # Download and extract
    if ! curl -fsSL -o "$filename" "$download_url"; then
        print_error "Failed to download IPFS CLI"
        rm -rf "$tmp_dir"
        exit 1
    fi
    
    print_info "Extracting IPFS archive..."
    tar -xzf "$filename"
    
    # Verify checksum (if available)
    if [ -f "kubo/ipfs" ]; then
        print_info "IPFS binary extracted successfully"
    else
        print_error "Failed to extract IPFS binary"
        rm -rf "$tmp_dir"
        exit 1
    fi
    
    # Install to /usr/local/bin or ~/bin
    if [ -w "/usr/local/bin" ]; then
        print_info "Installing IPFS to /usr/local/bin..."
        # Copy binary directly instead of running install.sh with sudo
        sudo cp kubo/ipfs /usr/local/bin/ipfs
        sudo chmod +x /usr/local/bin/ipfs
    else
        print_info "Installing IPFS to ~/bin (no sudo access)..."
        mkdir -p "$HOME/bin"
        cp kubo/ipfs "$HOME/bin/"
        chmod +x "$HOME/bin/ipfs"
        export PATH="$HOME/bin:$PATH"
        print_warning "Added ~/bin to PATH. You may need to add this to your shell profile."
    fi
    
    # Cleanup
    cd /
    rm -rf "$tmp_dir"
    
    # Verify installation
    if command -v ipfs &> /dev/null; then
        print_success "IPFS CLI installed successfully: $(ipfs --version)"
    else
        print_error "IPFS installation failed"
        exit 1
    fi
}

#########################################
# Step 2: Initialize and Start IPFS Daemon
#########################################

initialize_ipfs() {
    print_section "Step 2: IPFS Initialization"
    
    if [ -d "$IPFS_DIR" ]; then
        print_success "IPFS repository already initialized at $IPFS_DIR"
    else
        print_info "Initializing IPFS repository..."
        if ! ipfs init; then
            print_error "Failed to initialize IPFS repository"
            exit 1
        fi
        print_success "IPFS repository initialized successfully"
    fi
}

start_ipfs_daemon() {
    print_section "Step 3: Starting IPFS Daemon"
    
    # Check if daemon is already running
    if ipfs swarm peers &> /dev/null; then
        print_success "IPFS daemon is already running"
        return 0
    fi
    
    print_info "Starting IPFS daemon in background..."
    
    # Start daemon in background
    nohup ipfs daemon > /tmp/ipfs-daemon.log 2>&1 &
    local daemon_pid=$!
    
    print_info "IPFS daemon started with PID: $daemon_pid"
    print_info "Waiting for daemon to be ready..."
    
    # Wait for daemon to be ready (max 30 seconds)
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if ipfs swarm peers &> /dev/null; then
            print_success "IPFS daemon is ready"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
        echo -n "."
    done
    
    echo ""
    print_error "IPFS daemon failed to start within 30 seconds"
    print_info "Check logs at /tmp/ipfs-daemon.log"
    exit 1
}

#########################################
# Step 4: Add Documentation to IPFS
#########################################

add_to_ipfs() {
    print_section "Step 4: Adding Documentation to IPFS"
    
    # Check if docs directory exists
    if [ ! -d "$DOCS_DIR" ]; then
        print_error "Documentation directory '$DOCS_DIR' not found!"
        print_info "Please create a '$DOCS_DIR' directory in the repository root with your documentation."
        exit 1
    fi
    
    # Check if directory is empty
    if [ -z "$(ls -A $DOCS_DIR)" ]; then
        print_error "Documentation directory '$DOCS_DIR' is empty!"
        print_info "Please add documentation files to the '$DOCS_DIR' directory."
        exit 1
    fi
    
    print_info "Adding contents of '$DOCS_DIR' directory to IPFS..."
    
    # Add directory recursively to IPFS and capture output
    local ipfs_output=$(ipfs add -r "$DOCS_DIR" 2>&1)
    
    # Display output to user
    echo "$ipfs_output"
    
    # Extract the CID of the root directory (last line)
    local cid=$(echo "$ipfs_output" | tail -n 1 | awk '{print $2}')
    
    if [ -z "$cid" ]; then
        print_error "Failed to extract CID from IPFS output"
        exit 1
    fi
    
    print_success "Documentation added to IPFS successfully!"
    print_info "Content Identifier (CID): $cid"
    print_info "IPFS Gateway URL: https://ipfs.io/ipfs/$cid"
    
    # Return CID for next step
    echo "$cid"
}

#########################################
# Step 5: Pin to Pinata
#########################################

pin_to_pinata() {
    local cid=$1
    
    print_section "Step 5: Pinning to Pinata"
    
    # Check for PINATA_JWT
    if [ -z "$PINATA_JWT" ]; then
        print_error "PINATA_JWT environment variable is not set!"
        print_info "Please export your Pinata JWT token:"
        print_info "  export PINATA_JWT=\"your_pinata_jwt_token\""
        exit 1
    fi
    
    print_info "Pinning CID to Pinata: $cid"
    
    # Prepare JSON payload
    local payload=$(cat <<EOF
{
  "hashToPin": "$cid",
  "pinataMetadata": {
    "name": "Euystacio Documentation - $(date +%Y-%m-%d)"
  }
}
EOF
)
    
    # Make API request to Pinata using a header file to avoid exposing JWT in process list
    local header_file=$(mktemp)
    echo "Authorization: Bearer $PINATA_JWT" > "$header_file"
    
    local response=$(curl -s -w "\n%{http_code}" -X POST \
        "https://api.pinata.cloud/pinning/pinByHash" \
        -H @"$header_file" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    # Clean up header file
    rm -f "$header_file"
    
    # Extract HTTP status code and response body
    local http_code=$(echo "$response" | tail -n 1)
    local response_body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        print_success "Content successfully pinned to Pinata!"
        print_info "Response: $response_body"
    else
        print_error "Failed to pin to Pinata (HTTP $http_code)"
        print_error "Response: $response_body"
        exit 1
    fi
}

#########################################
# Main Execution Flow
#########################################

main() {
    print_section "Euystacio IPFS Eternalization"
    print_info "Starting automated IPFS eternalization workflow..."
    
    # Step 1: Install IPFS CLI if needed
    install_ipfs
    
    # Step 2: Initialize IPFS
    initialize_ipfs
    
    # Step 3: Start IPFS daemon
    start_ipfs_daemon
    
    # Step 4: Add documentation to IPFS
    local cid=$(add_to_ipfs)
    
    # Step 5: Pin to Pinata
    pin_to_pinata "$cid"
    
    # Final summary
    print_section "Eternalization Complete!"
    print_success "Your documentation has been eternalized on IPFS and Pinata"
    print_info "CID: $cid"
    print_info "Gateway URL: https://ipfs.io/ipfs/$cid"
    print_info "Pinata Gateway: https://gateway.pinata.cloud/ipfs/$cid"
    
    echo ""
    print_info "Next steps:"
    print_info "  1. Share the CID with your community"
    print_info "  2. Add the CID to your documentation"
    print_info "  3. Consider adding the gateway URL to your README"
    echo ""
}

# Run main function
main
