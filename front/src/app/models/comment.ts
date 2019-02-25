import { User } from './user';

export class Comment {
    id: number;
    idPost: number;
    idParentComment: number;
    body: string;
    path: string;
    updatedAt: string;
    createdAt: string;
    writer: User;
}