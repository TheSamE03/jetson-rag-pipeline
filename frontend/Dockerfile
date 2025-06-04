FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
# This takes advantage of Docker layer caching
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# Expose the port the app runs on (if serving with Nginx later, this might be different)
# For react-scripts start, it's typically 3000. For Nginx serving build, it's 80.
EXPOSE 3000

# The command to start the app (development server)
# For production, you'd typically serve the 'build' folder with Nginx or similar
CMD ["npm", "start"] 