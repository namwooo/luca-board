import { User } from './user';

export class Comment {
    id: number;
    idWriter: number;
    idPost: number;
    idParentComment: number;
    body: string;
    path: string;
    updatedAt: string;
    createdAt: string;
    writer: User;
}

export class CommentForm {
    body: string;
}