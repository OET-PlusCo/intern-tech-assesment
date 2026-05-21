# Assessment frontend — Node + Express serving static HTML
FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --omit=dev

COPY frontend/ ./

# BUG 1 (intentional): build args are declared but Cloud Build does not pass them yet.
# Candidate should wire: substitutions → docker build --build-arg → npm run build
ARG APP_GREETING=unset
ARG CLIENT_ID=unknown
ENV APP_GREETING=${APP_GREETING}
ENV CLIENT_ID=${CLIENT_ID}

RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/server.js ./
COPY --from=build /app/public ./public
COPY --from=build /app/package.json ./

ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
