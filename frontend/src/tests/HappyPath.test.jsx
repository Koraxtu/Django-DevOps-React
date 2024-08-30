import { screen, render } from "@testing-library/react";
import { act } from "react";
import userEvent from "@testing-library/user-event";
import App from "../App";

test("Happy path test", async () => {
  await act(async () => {
    render(<App />);
  });
  const copyrightText = await screen.findAllByText(/copyright/i);
  expect(copyrightText.length).toBeGreaterThan(0);
});
