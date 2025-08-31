import { message } from "@/interfaces/interfaces";
import { Bot, SparklesIcon, User } from "lucide-react";
import { Markdown } from "./markdown";
import { Button } from "../ui/button";
import { useState } from "react";
import { IntermediateSteps } from "./IntermediateSteps";
import { ChevronDown, ChevronUp } from 'lucide-react';
import { motion } from "framer-motion";
import { cx } from "class-variance-authority";


export function PreviewMessage({ message }: { message: message }) {
  const [showSteps, setShowSteps] = useState(false);
  const isAssistant = message.role === "assistant";

  return (
    <div className="flex flex-col group md:items-center">
      <div className="flex gap-4 p-4 md:max-w-3xl md:w-full">
        <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-primary shrink-0">
          {isAssistant ? <Bot size={20} /> : <User size={20} />}
        </div>
        <div className="flex flex-col min-w-0 w-full">
          <div className="font-semibold">
            {isAssistant ? "Assistant" : "You"}
          </div>
          <div className="min-w-0">
            <Markdown>{message.content}</Markdown>
          </div>
          {isAssistant && message.intermediate_steps && message.intermediate_steps.length > 0 && (
            <div className="mt-2">
              <Button variant="outline" size="sm" onClick={() => setShowSteps(!showSteps)}>
                {showSteps ? "Hide Steps" : "Show Steps"}
                {showSteps ? <ChevronUp className="ml-2 h-4 w-4" /> : <ChevronDown className="ml-2 h-4 w-4" />}
              </Button>
            </div>
          )}
        </div>
      </div>
      {showSteps && message.intermediate_steps && (
        <div className="p-4 pt-0 md:max-w-3xl md:w-full md:pl-[64px]">
            <IntermediateSteps steps={message.intermediate_steps} finalAnswer={message.content} />
        </div>
      )}
    </div>
  );
}

export function ThinkingMessage() {
  const role = 'assistant';

  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message "
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 0.2 } }}
      data-role={role}
    >
      <div
        className={cx(
          'flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl',
          'group-data-[role=user]/message:bg-muted'
        )}
      >
        <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
          <SparklesIcon size={14} />
        </div>
      </div>
    </motion.div>
  );
};
