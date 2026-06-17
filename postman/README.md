# Postman Assets

This folder contains importable Postman files for the current admin backend.

## Files

- `TheTechProjectAdmin.postman_collection.json`
- `TheTechProjectLocal.postman_environment.json`

## Import

1. Open Postman.
2. Click `Import`.
3. Import both files from this folder.
4. Select the environment `The Tech Project Local`.
5. Start with `Auth > Login`.

## Default local values

- `baseUrl`: `http://127.0.0.1:8000`
- `username`: `superadmin`
- `password`: `Tech@1234`

## API List

### Health

- `GET /api/v1/health`

### Auth

- `POST /api/v1/admin/auth/login`
- `GET /api/v1/admin/auth/login-user-details`

### Users

- `GET /api/v1/admin/users`
- `POST /api/v1/admin/users`
- `GET /api/v1/admin/users/{userId}`
- `PUT /api/v1/admin/users/{userId}`
- `DELETE /api/v1/admin/users/{userId}`

### Dashboard

- `GET /api/v1/admin/dashboard/summary`
- `GET /api/v1/admin/dashboard/top-blogs`

### Blogs

- `GET /api/v1/admin/blogs`
- `POST /api/v1/admin/blogs`
- `POST /api/v1/admin/blogs/preview`
- `GET /api/v1/admin/blogs/{blogId}`
- `PUT /api/v1/admin/blogs/{blogId}`
- `PATCH /api/v1/admin/blogs/{blogId}/status`
- `DELETE /api/v1/admin/blogs/{blogId}`

### Assets

- `GET /api/v1/admin/assets`
- `POST /api/v1/admin/assets`
- `GET /api/v1/admin/assets/{assetId}`
- `DELETE /api/v1/admin/assets/{assetId}`

### Categories

- `GET /api/v1/admin/categories`
- `POST /api/v1/admin/categories`
- `GET /api/v1/admin/categories/{categoryId}`
- `PUT /api/v1/admin/categories/{categoryId}`
- `DELETE /api/v1/admin/categories/{categoryId}`

### Tags

- `GET /api/v1/admin/tags`
- `POST /api/v1/admin/tags`
- `GET /api/v1/admin/tags/{tagId}`
- `PUT /api/v1/admin/tags/{tagId}`
- `DELETE /api/v1/admin/tags/{tagId}`

### Analytics

- `GET /api/v1/admin/analytics/overview`
- `GET /api/v1/admin/analytics/blogs`
- `GET /api/v1/admin/analytics/blogs/{blogId}`

### Master

- `GET /api/v1/admin/master/blog-statuses`

## Suggested execution order

1. `Auth > Login`
2. `Master > List Blog Statuses`
3. `Users > Create User`
4. `Categories > Create Category`
5. `Tags > Create Tag`
6. `Blogs > Create Blog`
7. `Dashboard` and `Analytics` requests

The collection automatically stores `accessToken`, `userId`, `categoryId`, `tagId`, `blogId`, and `assetId` from create responses when available.
