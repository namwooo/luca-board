export class PostForm {
    is_published: boolean;
    board_id: number;
    title: string;
    body: string;

    constructor(is_published: boolean) {
        this.is_published = is_published;
    }
}