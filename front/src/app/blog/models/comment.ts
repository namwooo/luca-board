import { Member } from 'src/app/member/models/member';


export class Comment {
    id: number;
    idWriter: number;
    idPost: number;
    idParentComment: number;
    body: string;
    path: string;
    updatedAt: string;
    createdAt: string;
    writer: Member;
}

export class CommentForm {
    body: string;
}