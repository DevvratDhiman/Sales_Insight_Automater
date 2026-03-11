# Use official Node image
FROM node:20

# Set working dir
WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY . .

# Build production frontend
RUN npm run build

# Serve using simple server
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Run frontend
CMD ["serve", "-s", "build", "-l", "3000"]