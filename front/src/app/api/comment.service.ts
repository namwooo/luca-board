import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Comment } from '../blog/models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private baseUrl = 'http://localhost:5000/';

  constructor(
    private http: HttpClient,
  ) { }

  getCommentsInPost(idPost: number): Observable<Comment[]> {
    const url = this.baseUrl + `posts/${idPost}/comments`;
    return this.http.get<Comment[]>(url)
    .pipe(
      catchError(this.handleError<Comment[]>(`getPostsInBoard`))
      )
  }

  createComment(commentForm: any, postId: number, targetComment: Comment): Observable<Comment> {
    let url;
    if (targetComment) {
      let commentId = targetComment.id
      url = this.baseUrl + `comments?postId=${postId}&commentId=${commentId}`;
    } else {
      url = this.baseUrl + `comments?postId=${postId}`;
    }

    let token = this.getToken();
    return this.http.post<Comment>(url, commentForm, { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError<Comment>(`createComment`))
    )
  }

  deleteComment(commentId: number) {
    const url = this.baseUrl + `comments/${commentId}`;
    let token = this.getToken();
    return this.http.delete(url, { headers: new HttpHeaders().set('Authorization', `Bearer ${token}`) })
    .pipe(
      catchError(this.handleError(`deleteComment`))
    )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error('error'); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  private getToken() {
    return localStorage.getItem('access_token')
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  withCredentials: true
};