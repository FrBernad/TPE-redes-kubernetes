import React from "react";
import { queryClient } from "@/config/reactQueryConfig.js";
import { QueryClientProvider } from "@tanstack/react-query";

export const DefaultLayout = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen flex flex-col">{children}</div>
    </QueryClientProvider>
  );
};
