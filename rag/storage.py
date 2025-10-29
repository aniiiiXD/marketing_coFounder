"""
Storage Service

Handles all file storage operations, primarily with S3, including:
- File uploads and downloads
- Version control for documents
- Secure URL generation
- File organization and management
- Large file handling with multipart uploads

This service provides a unified interface for persistent storage needs
across the application, abstracting away the underlying storage provider.
"""
