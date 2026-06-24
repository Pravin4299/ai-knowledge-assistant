from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    @staticmethod
    def create(
        db: Session,
        document: Document
    ):
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_user_documents(
        db: Session,
        user_id: str
    ):
        return (
            db.query(Document)
            .filter(
                Document.user_id == user_id,
                Document.is_deleted == False
            )
            .order_by(
                Document.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: str
    ):
        return (
            db.query(Document)
            .filter(
                Document.id == document_id,
                Document.is_deleted == False
            )
            .first()
        )

    @staticmethod
    def delete(
        db,
        document
    ):
        db.delete(document)
        db.commit()

    @staticmethod
    def get_by_id(
        db,
        document_id: str
    ):
        return (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )
    
    @staticmethod
    def get_user_documents(
        db,
        user_id: str
    ):
        return (
            db.query(Document)
            .filter(
                Document.user_id == user_id
            )
            .order_by(
                Document.created_at.desc()
            )
            .all()
        )
    
    @staticmethod
    def update_status(
        db,
        document,
        status: str
    ):
        document.processing_status = status

        db.commit()
        db.refresh(document)

        return document
    