import { Member } from 'src/app/member/models/member';


export class Post {
    id: number;
    board_id: number;
    title: string;
    body: string;
is_published: boolean;
    like_count: number;
    view_count: number;
    updated_at: string;
    created_at: string;
    writer: Member;

    constructor(){
        this.is_published = true;
    }
}

export class PostForm {
    idBoard: number;
    title: string;
    body: string;
    isPublished: boolean;
}