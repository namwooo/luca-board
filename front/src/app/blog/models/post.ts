export class PagedPost {

    constructor(
        public page: number,
        public perPage: number,
        public total: number,
        public items: Post[],
    ){}

    getBoardTitle() {
        // return this.items[0].board.title
    }
}

export class Post {
    
    constructor(
        public id: number,
        public title: string,
        public body: string,
        public hasImage: boolean,
        public isPublished: boolean,
        public likeCount: number,
        public viewCount: number,
        public createdAt: string,
        public updatedAt: string,
        public board: Board,
        public writer: Writer,
    ) {
        this.isPublished = true;
    }
}

// interface Post {
//     id: number,
//     title: string,
//     body: string,
//     hasImage: boolean,
//     isPublished: boolean,
//     likeCount: number,
//     viewCount: number,
//     createdAt: string,
//     updatedAt: string,
//     board: Board,
//     writer: Writer,
// }

interface Board {
    id: number;
    title: string;
}

interface Writer {
    id: number;
    name: string;
}