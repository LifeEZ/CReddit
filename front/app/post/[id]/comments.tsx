"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { ArrowBigDown, ArrowBigUp } from "lucide-react";
import { formatNumber } from "@/lib/utils";
import { Comment } from "@/lib/types";
import { format } from "date-fns";

function CommentComponent({ comment }: { comment: Comment }) {
  const [votes, setVotes] = useState(comment.votes);

  return (
    <div className="pl-4 border-l-2 border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
        <span className="font-medium text-gray-900 dark:text-white">u/{comment.author}</span>
        <span>•</span>
        <span>{format(new Date(comment.createdAt), 'MMM d, yyyy')}</span>
      </div>
      <p className="mt-2 text-gray-700 dark:text-gray-300">{comment.content}</p>
      <div className="mt-2 flex items-center gap-2">
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={() => setVotes(v => v + 1)}
        >
          <ArrowBigUp className="h-4 w-4" />
        </Button>
        <span className="text-sm font-medium">{formatNumber(votes)}</span>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={() => setVotes(v => v - 1)}
        >
          <ArrowBigDown className="h-4 w-4" />
        </Button>
      </div>
      {comment.replies && (
        <div className="mt-4 space-y-4">
          {comment.replies.map(reply => (
            <CommentComponent key={reply.id} comment={reply} />
          ))}
        </div>
      )}
    </div>
  );
}

export function Comments({ comments }) {
  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Comments ({comments.length})</h2>
      <Separator className="mb-6" />
      <div className="space-y-6">
        {comments.map(comment => (
          <CommentComponent key={comment.id} comment={comment} />
        ))}
      </div>
    </Card>
  );
}