async function getMessage() {
  const response = await fetch("http://127.0.0.1:8000/api/hello/");

  if (!response.ok) {
    throw new Error("Failed to fetch message");
  }

  return response.json();
}

export default async function Home() {
  const data = await getMessage();

  return (
    <main>
      <h1>{data.message}</h1>
    </main>
  );
}
