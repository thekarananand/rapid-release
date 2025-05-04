FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run lint -- --max-warnings 0
RUN npm run build

FROM node:22-alpine AS production
WORKDIR /app
COPY --from=build /app ./
RUN npm ci --omit=dev
EXPOSE 3000
CMD ["npm", "start"]