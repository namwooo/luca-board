import { User } from './user';

export class Post {
    id: number;
    title: string;
    body: string;
    is_published: boolean;
    like_count: number;
    view_count: number;
    updated_at: string;
    created_at: string;
    writer: User;
}