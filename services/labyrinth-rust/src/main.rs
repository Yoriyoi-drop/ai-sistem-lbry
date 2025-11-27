use actix_web::{get, App, HttpResponse, HttpServer, Responder};
use serde_json::json;

#[get("/analyze")]
async fn analyze() -> impl Responder {
    HttpResponse::Ok().json(json!({
        "status": "ok",
        "message": "Analysis completed",
        "service": "labyrinth-rust"
    }))
}

#[get("/health")]
async fn health() -> impl Responder {
    HttpResponse::Ok().json(json!({
        "status": "healthy",
        "service": "labyrinth-rust"
    }))
}

#[get("/metrics")]
async fn metrics() -> impl Responder {
    // Simple metrics placeholder
    let metrics_text = r#"
# HELP labyrinth_analyze_total Total number of analyze requests
# TYPE labyrinth_analyze_total counter
labyrinth_analyze_total 0
"#;
    HttpResponse::Ok()
        .content_type("text/plain; version=0.0.4")
        .body(metrics_text)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    
    log::info!("🦀 Labyrinth service starting on :8003");
    
    HttpServer::new(|| {
        App::new()
            .service(health)
            .service(analyze)
            .service(metrics)
    })
    .bind(("0.0.0.0", 8003))?
    .run()
    .await
}
