FROM node:18-alpine

WORKDIR /app

# Ensure proper ownership of the working directory
RUN chown -R node:node /app

# Copy package files first to leverage cache
COPY --chown=node:node package*.json ./

# Switch to non-root user
USER node

# Install dependencies as non-root user
RUN npm install

# Copy the rest of the application code
COPY --chown=node:node . .

CMD ["npm", "run", "dev", "--", "--host"]
