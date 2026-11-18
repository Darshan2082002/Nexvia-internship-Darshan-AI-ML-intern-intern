FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5174

# Run the Vite dev server exposing it to the Docker network
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5174"]