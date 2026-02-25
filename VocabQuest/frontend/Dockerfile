FROM node:18-alpine

WORKDIR /app

# Ensure proper ownership of the working directory
RUN chown -R node:node /app

# Switch to non-root user
USER node

COPY --chown=node:node package*.json ./
RUN npm install

COPY --chown=node:node . .

CMD ["npm", "run", "dev", "--", "--host"]
