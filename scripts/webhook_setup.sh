#!/bin/bash
#
# Webhook Setup Script for Framework Euystacio
# Configures webhook integration between GitHub and Discord/Telegram
#
# Usage: ./webhook_setup.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Framework Euystacio Webhook Setup${NC}"
echo "====================================="
echo ""

# Configuration file
CONFIG_FILE=".webhooks.config"

# Function to setup Discord webhook
setup_discord() {
    echo -e "${BLUE}Discord Webhook Setup${NC}"
    echo "----------------------"
    echo ""
    
    echo "To create a Discord webhook:"
    echo "1. Go to your Discord server settings"
    echo "2. Navigate to Integrations > Webhooks"
    echo "3. Click 'New Webhook'"
    echo "4. Name it 'Framework Euystacio Bot'"
    echo "5. Select the channel for notifications"
    echo "6. Copy the webhook URL"
    echo ""
    
    read -p "Enter Discord Webhook URL: " DISCORD_WEBHOOK
    
    if [[ -z "$DISCORD_WEBHOOK" ]]; then
        echo -e "${RED}Error: Webhook URL cannot be empty${NC}"
        return 1
    fi
    
    echo "DISCORD_WEBHOOK=$DISCORD_WEBHOOK" >> "$CONFIG_FILE"
    
    # Test webhook
    echo "Testing Discord webhook..."
    
    PAYLOAD=$(cat <<EOF
{
  "embeds": [{
    "title": "🌟 Framework Euystacio - Webhook Test",
    "description": "Webhook integration successfully configured!",
    "color": 3447003,
    "fields": [
      {
        "name": "Status",
        "value": "✅ Active",
        "inline": true
      },
      {
        "name": "Type",
        "value": "Discord Integration",
        "inline": true
      }
    ],
    "footer": {
      "text": "Seedbringer Treasury | Framework Euystacio"
    },
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }]
}
EOF
)
    
    RESPONSE=$(curl -s -H "Content-Type: application/json" \
        -d "$PAYLOAD" \
        "$DISCORD_WEBHOOK")
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✓ Discord webhook configured successfully!${NC}"
        echo "Check your Discord channel for the test message."
    else
        echo -e "${RED}✗ Discord webhook test failed${NC}"
        echo "Response: $RESPONSE"
        return 1
    fi
    
    echo ""
}

# Function to setup Telegram webhook
setup_telegram() {
    echo -e "${BLUE}Telegram Bot Setup${NC}"
    echo "------------------"
    echo ""
    
    echo "To create a Telegram bot:"
    echo "1. Open Telegram and search for @BotFather"
    echo "2. Send /newbot and follow instructions"
    echo "3. Copy the bot token"
    echo "4. Add the bot to your channel"
    echo "5. Get your channel ID (use @userinfobot)"
    echo ""
    
    read -p "Enter Telegram Bot Token: " TELEGRAM_TOKEN
    read -p "Enter Telegram Channel ID: " TELEGRAM_CHAT_ID
    
    if [[ -z "$TELEGRAM_TOKEN" ]] || [[ -z "$TELEGRAM_CHAT_ID" ]]; then
        echo -e "${RED}Error: Bot token and chat ID are required${NC}"
        return 1
    fi
    
    echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> "$CONFIG_FILE"
    echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> "$CONFIG_FILE"
    
    # Test bot
    echo "Testing Telegram bot..."
    
    MESSAGE="🌟 Framework Euystacio - Webhook Test\n\n✅ Telegram integration successfully configured!\n\nSeedbringer Treasury"
    
    RESPONSE=$(curl -s -X POST \
        "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${MESSAGE}" \
        -d "parse_mode=HTML")
    
    if echo "$RESPONSE" | grep -q '"ok":true'; then
        echo -e "${GREEN}✓ Telegram bot configured successfully!${NC}"
        echo "Check your Telegram channel for the test message."
    else
        echo -e "${RED}✗ Telegram bot test failed${NC}"
        echo "Response: $RESPONSE"
        return 1
    fi
    
    echo ""
}

# Function to create notification script
create_notification_script() {
    echo -e "${BLUE}Creating notification script...${NC}"
    
    cat > scripts/send_notification.sh <<'NOTIFYSCRIPT'
#!/bin/bash
#
# Send notifications to Discord and/or Telegram
# Usage: ./send_notification.sh "Title" "Message" [type]
#

set -e

TITLE="$1"
MESSAGE="$2"
TYPE="${3:-info}"  # info, success, error, warning

# Load configuration
if [[ -f .webhooks.config ]]; then
    source .webhooks.config
fi

# Color codes for embed
case "$TYPE" in
    success) COLOR=3066993 ;; # Green
    error) COLOR=15158332 ;; # Red
    warning) COLOR=15105570 ;; # Orange
    *) COLOR=3447003 ;; # Blue
esac

# Icon for type
case "$TYPE" in
    success) ICON="✅" ;;
    error) ICON="❌" ;;
    warning) ICON="⚠️" ;;
    *) ICON="ℹ️" ;;
esac

# Send to Discord
if [[ -n "$DISCORD_WEBHOOK" ]]; then
    PAYLOAD=$(cat <<EOF
{
  "embeds": [{
    "title": "$ICON $TITLE",
    "description": "$MESSAGE",
    "color": $COLOR,
    "footer": {
      "text": "Framework Euystacio | Seedbringer Treasury"
    },
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }]
}
EOF
)
    
    curl -s -H "Content-Type: application/json" \
        -d "$PAYLOAD" \
        "$DISCORD_WEBHOOK" > /dev/null
    
    echo "✓ Sent to Discord"
fi

# Send to Telegram
if [[ -n "$TELEGRAM_TOKEN" ]] && [[ -n "$TELEGRAM_CHAT_ID" ]]; then
    TELEGRAM_MESSAGE="$ICON <b>$TITLE</b>\n\n$MESSAGE\n\n<i>Framework Euystacio | Seedbringer Treasury</i>"
    
    curl -s -X POST \
        "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${TELEGRAM_MESSAGE}" \
        -d "parse_mode=HTML" > /dev/null
    
    echo "✓ Sent to Telegram"
fi
NOTIFYSCRIPT

    chmod +x scripts/send_notification.sh
    echo -e "${GREEN}✓ Notification script created: scripts/send_notification.sh${NC}"
    echo ""
}

# Function to create GitHub Actions workflow
create_github_workflow() {
    echo -e "${BLUE}Creating GitHub Actions workflow...${NC}"
    
    mkdir -p .github/workflows
    
    cat > .github/workflows/notification_propagation.yml <<'WORKFLOW'
name: Notification Propagation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]
  issues:
    types: [ opened, closed ]

jobs:
  notify:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup notification script
        run: |
          chmod +x scripts/send_notification.sh
      
      - name: Notify on Push
        if: github.event_name == 'push'
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          echo "DISCORD_WEBHOOK=$DISCORD_WEBHOOK" > .webhooks.config
          echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> .webhooks.config
          echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .webhooks.config
          
          ./scripts/send_notification.sh \
            "New Commit to Main" \
            "Commit: ${{ github.event.head_commit.message }}\nAuthor: ${{ github.event.head_commit.author.name }}\nSHA: ${{ github.sha }}" \
            "info"
      
      - name: Notify on Release
        if: github.event_name == 'release'
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          echo "DISCORD_WEBHOOK=$DISCORD_WEBHOOK" > .webhooks.config
          echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> .webhooks.config
          echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .webhooks.config
          
          ./scripts/send_notification.sh \
            "New Release: ${{ github.event.release.name }}" \
            "${{ github.event.release.body }}" \
            "success"
      
      - name: Notify on Issue Opened
        if: github.event_name == 'issues' && github.event.action == 'opened'
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          echo "DISCORD_WEBHOOK=$DISCORD_WEBHOOK" > .webhooks.config
          echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> .webhooks.config
          echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .webhooks.config
          
          ./scripts/send_notification.sh \
            "New Issue: ${{ github.event.issue.title }}" \
            "Opened by: ${{ github.event.issue.user.login }}\nURL: ${{ github.event.issue.html_url }}" \
            "warning"
WORKFLOW

    echo -e "${GREEN}✓ GitHub Actions workflow created: .github/workflows/notification_propagation.yml${NC}"
    echo ""
}

# Function to setup GitHub secrets
setup_github_secrets() {
    echo -e "${BLUE}GitHub Secrets Setup${NC}"
    echo "--------------------"
    echo ""
    
    echo "You need to add the following secrets to your GitHub repository:"
    echo ""
    echo "1. Go to: https://github.com/hannesmitterer/Euystacio/settings/secrets/actions"
    echo "2. Click 'New repository secret'"
    echo "3. Add these secrets:"
    echo ""
    
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
        
        if [[ -n "$DISCORD_WEBHOOK" ]]; then
            echo -e "   ${YELLOW}DISCORD_WEBHOOK${NC}"
            echo "   Value: $DISCORD_WEBHOOK"
            echo ""
        fi
        
        if [[ -n "$TELEGRAM_TOKEN" ]]; then
            echo -e "   ${YELLOW}TELEGRAM_TOKEN${NC}"
            echo "   Value: $TELEGRAM_TOKEN"
            echo ""
        fi
        
        if [[ -n "$TELEGRAM_CHAT_ID" ]]; then
            echo -e "   ${YELLOW}TELEGRAM_CHAT_ID${NC}"
            echo "   Value: $TELEGRAM_CHAT_ID"
            echo ""
        fi
    fi
    
    echo "After adding secrets, the GitHub Actions workflow will automatically"
    echo "send notifications to your configured channels."
    echo ""
}

# Main menu
main_menu() {
    while true; do
        echo ""
        echo "Select an option:"
        echo "1) Setup Discord webhook"
        echo "2) Setup Telegram bot"
        echo "3) Create notification script"
        echo "4) Create GitHub Actions workflow"
        echo "5) Show GitHub secrets instructions"
        echo "6) Test notifications"
        echo "7) Exit"
        echo ""
        read -p "Choice: " choice
        
        case $choice in
            1) setup_discord ;;
            2) setup_telegram ;;
            3) create_notification_script ;;
            4) create_github_workflow ;;
            5) setup_github_secrets ;;
            6) test_notifications ;;
            7) echo "Exiting..."; exit 0 ;;
            *) echo -e "${RED}Invalid choice${NC}" ;;
        esac
    done
}

# Test notifications
test_notifications() {
    echo -e "${BLUE}Testing notifications...${NC}"
    
    if [[ ! -f scripts/send_notification.sh ]]; then
        echo -e "${RED}Error: Notification script not found. Create it first (option 3)${NC}"
        return 1
    fi
    
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
    fi
    
    ./scripts/send_notification.sh \
        "Test Notification" \
        "This is a test message from the webhook setup script." \
        "info"
    
    echo -e "${GREEN}✓ Test notifications sent${NC}"
}

# Run main menu
main_menu
