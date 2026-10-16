export default function App() {
  return (
    <main>
      <p className="eyebrow">Wallet MVP</p>
      <h1>Servicios locales listos</h1>
      <p className="description">
        La interfaz React esta ejecutandose en Node y el backend Flask se conecta
        a PostgreSQL.
      </p>
      <a href="http://localhost:5000/health">Consultar salud del backend</a>
    </main>
  );
}