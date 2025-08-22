#!/bin/bash

# MongoDB Docker Setup Guide for Music News Analyzer
# Run this step by step in your terminal

echo "🎵 Setting up MongoDB with Docker for Music News Analyzer"

# Step 1: Check if Docker is installed
echo "📋 Step 1: Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
else
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Step 2: Start Docker service
echo "🚀 Step 2: Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Step 3: Check if container already exists
echo "🔍 Step 3: Checking for existing MongoDB container..."
if docker ps -a --format 'table {{.Names}}' | grep -q mongodb; then
    echo "⚠️  MongoDB container already exists"
    echo "Current status:"
    docker ps -a --filter name=mongodb --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    read -p "Do you want to remove the existing container and create a new one? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing container..."
        docker stop mongodb 2>/dev/null || true
        docker rm mongodb 2>/dev/null || true
    else
        echo "✅ Keeping existing container. Starting if stopped..."
        docker start mongodb
        exit 0
    fi
fi

# Step 4: Pull MongoDB image
echo "📥 Step 4: Pulling MongoDB Docker image..."
docker pull mongo:7.0

# Step 5: Create MongoDB container with proper configuration
echo "🛠️  Step 5: Creating MongoDB container..."
docker run -d \
    --name mongodb \
    -p 27018:27017 \
    -v mongodb_data:/data/db \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=admin123 \
    -e MONGO_INITDB_DATABASE=music_news_db \
    --restart unless-stopped \
    mongo:7.0

# Wait for MongoDB to start
echo "⏳ Step 6: Waiting for MongoDB to start..."
sleep 5

# Step 7: Verify MongoDB is running
echo "✅ Step 7: Verifying MongoDB container..."
if docker ps --filter name=mongodb --format 'table {{.Names}}\t{{.Status}}' | grep -q mongodb; then
    echo "🎉 MongoDB container is running successfully!"
    docker ps --filter name=mongodb --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    echo "❌ MongoDB container failed to start. Checking logs..."
    docker logs mongodb
    exit 1
fi

# Step 8: Test MongoDB connection
echo "🧪 Step 8: Testing MongoDB connection..."
docker exec mongodb mongosh --eval "db.adminCommand('ping')" --quiet

echo ""
echo "🎵 MongoDB Setup Complete! 🎵"
echo "=================================="
echo "Container Name: mongodb"
echo "Port: 27018"
echo "Database: music_news_db"
echo "Username: admin"
echo "Password: admin123"
echo "Connection String: mongodb://admin:admin123@localhost:27018/music_news_db"
echo ""
echo "Useful Docker commands:"
echo "- Start container: docker start mongodb"
echo "- Stop container: docker stop mongodb"
echo "- View logs: docker logs mongodb"
echo "- MongoDB shell: docker exec -it mongodb mongosh"
echo "- Container status: docker ps --filter name=mongodb"
