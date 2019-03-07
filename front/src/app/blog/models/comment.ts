import { Member } from 'src/app/member/models/member';


export class Comment {
    id: number;
    postId: number;
    commentParentId: number;
    level: number;
    body: string;
    path: string;
    updatedAt: string;
    createdAt: string;
    writer: Member;
}

export class CommentForm {
    body: string;
}