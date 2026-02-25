FROM node:18-alpine

WORKDIR /app

# Ensure proper ownership of the working directory
RUN chown -R node:node /app

# Security: Switch to non-root user (node) to mitigate privilege escalation risks
USER node

COPY --chown=node:node package*.json ./
RUN npm install

COPY --chown=node:node . .

CMD ["npm", "run", "dev", "--", "--host"]
